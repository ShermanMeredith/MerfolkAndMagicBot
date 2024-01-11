from os import environ

import discord
from discord.ext import commands

from utils.accounts import user_accounts
import utils.database as database

# Config Variables
DESCRIPTION = "How-to-play Information"
LOGIN_FIRST = f"""Looks like you aren't logged in right now...
Go to <#{database.get_login_channel_id(int(environ.get("GUILD_ID")))}> to sign up or log in, then try again"""
INFO_BASICS = """>>> - In this game, you can explore this text-based world.
- You can look around by typing '/look'.
- You can speak by typing '/say <>'. For example, '/say hello'
- You can go to a connected space by typing '/go <place>'. For example, '/go blacksmith'.
- There are items in the game that you can get and view in your inventory. You can equip weapons."""
INFO_COMBAT = """>>> - If there is an enemy nearby, you can engage in combat with it by typing '/attack <enemy>'.
- For example, if there is a Snake, you can type '/attack snake' to begin combat.
- Every player and NPC has the following stats: HP, Attack, Defense, and Speed.
- You can boost these stats by killing monsters, gaining EXP, and gaining Levels.
- You can check your stats any time by typing '/stats'
- When you engage in combat, you and the enemy attack each other automatically.
- You will attack using 4 Abilities that you can set in advance.
- You can set Abilities any time outside of combat by typing, '/set'.
- If you die, you lose Gold and Items."""
INFO_CRAFTING = """>>> - You can craft weapons at the Blacksmith in Mara.
- Ores used to craft weapons can be mined in the Mountains."""


#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCommand(bot))


#==================================================================================================
# HELP COMMAND
#==================================================================================================
class HelpCommand(commands.Cog, name="Help Command"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #----------------------------------------------------------------------------------------------
    # COMMAND: /help
    #----------------------------------------------------------------------------------------------
    @discord.app_commands.command(name='help', description=DESCRIPTION)
    async def help(self, interaction: discord.Interaction):
        print(f"Received /help command from {interaction.user.display_name}")

        # check whether user is logged in
        if interaction.user.id not in user_accounts:
            embed = discord.Embed(title="No Account Detected", description=LOGIN_FIRST)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        help_embed = discord.Embed(title="What do you need help with?")
        await interaction.response.send_message(embed=help_embed, view=HelpView(), ephemeral=True)


#==================================================================================================
# HELP VIEW
#==================================================================================================
class HelpView(discord.ui.View):
    #----------------------------------------------------------------------------------------------
    # BASICS BUTTON
    #----------------------------------------------------------------------------------------------
    @discord.ui.button(
        label="<Basics>",
        style=discord.ButtonStyle.blurple,
        row=0
    )
    async def button_help_basics(self, interaction: discord.Interaction, button: discord.ui.Button):
        basics_embed = discord.Embed(title="<Basics>", description=INFO_BASICS)
        await interaction.response.send_message(embed=basics_embed, ephemeral=True)

    #----------------------------------------------------------------------------------------------
    # COMBAT BUTTON
    #----------------------------------------------------------------------------------------------
    @discord.ui.button(
        label="<Combat>",
        style=discord.ButtonStyle.blurple,
        row=0
    )
    async def button_help_combat(self, interaction: discord.Interaction, button: discord.ui.Button):
        combat_embed = discord.Embed(title="<Combat>", description=INFO_COMBAT)
        await interaction.response.send_message(embed=combat_embed, ephemeral=True)

    #----------------------------------------------------------------------------------------------
    # CRAFTING BUTTON
    #----------------------------------------------------------------------------------------------
    @discord.ui.button(
        label="<Crafting>",
        style=discord.ButtonStyle.blurple,
        row=0
    )
    async def button_help_crafting(self, interaction: discord.Interaction, button: discord.ui.Button):
        crafting_embed = discord.Embed(title="<Crafting>", description=INFO_CRAFTING)
        await interaction.response.send_message(embed=crafting_embed, ephemeral=True)
