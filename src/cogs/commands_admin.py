# builtin modules
from os import environ
from io import StringIO

# installed modules
from discord import app_commands, Embed, Attachment, File, Interaction, utils, PermissionOverwrite
from discord.ext import commands
from eth_account.signers.local import LocalAccount
from eth_account import Account
from eth_keys.exceptions import ValidationError

# local modules
from utils.accounts import user_accounts
from login_panel import AccountManagementView

# Config Variables
GROUP_DESCRIPTION = "Admin-Only Commands"

#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))


#==================================================================================================
# ADMIN COG
#==================================================================================================
class AdminCog(commands.Cog, name="Admin Cog"):

    group_admin = app_commands.Group(
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
    # COMMAND: /create-login-panel
    #----------------------------------------------------------------------------------------------
    @group_admin.command(name='create-login-panel', description="Create a new login panel")
    @app_commands.describe(login_channel_name="Name of the signup channel that will be created")
    async def create_login_panel(self, interaction: Interaction, login_channel_name: str):
        print(f"Received Create Login Panel Command from {interaction.user.display_name}")

        panel_channel = utils.get(interaction.guild.channels, name=login_channel_name)
        if panel_channel:
            print("channel exists!")
            await interaction.response.send_message(
                f"Login Channel {login_channel_name} already exists."
                "\nDelete the channel first if you want to re-send the login panel"
            )
        if not panel_channel:
            print("channel does not exist!")
            channel_permissions = {
                interaction.guild.default_role: PermissionOverwrite(send_messages=False),
                interaction.guild.me: PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    send_messages_in_threads=True,
                    create_public_threads=True,
                    manage_messages=True,
                    manage_threads=True,
                    read_message_history=True,
                    embed_links = True
                )
            }
            print("creating text channel now!")
            panel_channel = await interaction.guild.create_text_channel(
                login_channel_name,
                topic="Manage Account Login",
                overwrites=channel_permissions
            )
            print("sending response now!")
            await panel_channel.send(view=AccountManagementView())
            await interaction.response.send_message(f"Channel Successfully Created: <#{panel_channel.id}>", ephemeral=True)
