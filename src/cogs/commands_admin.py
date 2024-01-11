# builtin modules
import json
from typing import Dict, Optional

# installed modules
import discord
from discord.ext import commands

# local modules
import utils.database as database
from login_panel import AccountManagementView

# Config Variables
GROUP_DESCRIPTION = "Admin-Only Commands"
WELCOME_TITLE = "**Welcome to Merfolk and Magic**"
WELCOME_MESSAGE = """In this game, you can explore, chat with your friends, go mining, craft weapons, and fight monsters.
If you ever need help, use the /help command.

To start, create a new account, or login to an existing account."""

#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))


#==================================================================================================
# ADMIN COG
#==================================================================================================
class AdminCog(commands.Cog, name="Admin Cog"):

    USER_PERMISSIONS = discord.PermissionOverwrite(send_messages=False)
    BOT_PERMISSIONS = discord.PermissionOverwrite(
        view_channel=True,
        send_messages=True,
        send_messages_in_threads=True,
        create_public_threads=True,
        manage_messages=True,
        manage_threads=True,
        read_message_history=True,
        embed_links = True
    )

    group_admin = discord.app_commands.Group(
        name="admin",
        description=GROUP_DESCRIPTION,
        default_permissions=None
    )

    #----------------------------------------------------------------------------------------------
    # INIT
    #----------------------------------------------------------------------------------------------
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #----------------------------------------------------------------------------------------------
    # COMMAND: /sync-commands
    #----------------------------------------------------------------------------------------------
    @group_admin.command(name='sync-commands', description="Sync commands to this server")
    async def sync_commands(self, interaction: discord.Interaction):
        await self.bot.tree.sync(guild=discord.Object(id=interaction.guild.id))
        await interaction.response.send_message("Commands Synced", ephemeral=True)


    #----------------------------------------------------------------------------------------------
    # COMMAND: /create-login-panel
    #----------------------------------------------------------------------------------------------
    @group_admin.command(name='create-login-panel', description="Create a new login panel")
    @discord.app_commands.describe(login_channel_name="Signup channel name")
    async def create_login_panel(self, interaction: discord.Interaction, login_channel_name: str):
        print(f"Received Create Login Panel Command from {interaction.user.display_name}")
        await interaction.response.defer(thinking=True, ephemeral=True)

        existing_login_channel: discord.TextChannel = database.get_login_channel(interaction.guild)
        if existing_login_channel:
            print("channel should already exist")
            if discord.utils.get(interaction.guild.channels, name=existing_login_channel):
                print("channel still exists!")
                await interaction.response.send_message(
                    f"{existing_login_channel.mention} is already your Login Channel."
                    "\nDelete it before creating a new one."
                )
                return
            else:
                print("channel is gone!")

        response = ""
        panel_channel = discord.utils.get(interaction.guild.channels, name=login_channel_name)

        if panel_channel:
            print("channel already exists!")
            await interaction.response.send_message(
                f"Login Channel {panel_channel.mention} already exists."
                "\nDelete the channel first if you want to re-send the login panel"
            )
            return

        print("channel does not exist! creating text channel now!")
        channel_permissions = {
            interaction.guild.default_role: self.USER_PERMISSIONS,
            interaction.guild.me: self.BOT_PERMISSIONS
        }
        panel_channel = await interaction.guild.create_text_channel(
            login_channel_name,
            topic="Manage Account Login",
            overwrites=channel_permissions
        )
        response = f"Channel Successfully Created: {panel_channel.mention}\n\n"

        welcome_embed = discord.Embed(title=WELCOME_TITLE, description=WELCOME_MESSAGE)
        file=discord.File("src/images/welcome.png")
        welcome_embed.set_image(url="attachment://welcome.png")
        login_panel = await panel_channel.send(file=file, embed=welcome_embed, view=AccountManagementView())
        response += f"Login Panel Successfully Created: [Login Panel]({login_panel.jump_url})"

        database.set_login_channel(interaction.guild.id, panel_channel.id)

        print("sending response!")
        await interaction.followup.send(f"Channel Successfully Created: <#{panel_channel.id}>", ephemeral=True)
