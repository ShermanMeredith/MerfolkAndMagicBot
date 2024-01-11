from os import environ

import discord
from discord.ext import commands

from utils.accounts import user_accounts
import utils.database as database
import utils.skale as skale
from data.locations import Locations

# Config Variables
DESCRIPTION = "Look at your surroundings"
LOGIN_FIRST = f"""Looks like you aren't logged in right now...
Go to <#{database.get_login_channel_id(int(environ.get("GUILD_ID")))}> to sign up or log in, then try again"""


#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(LookCommand(bot))


#==================================================================================================
# LOOK COMMAND
#==================================================================================================
class LookCommand(commands.Cog, name="Look Command"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #----------------------------------------------------------------------------------------------
    # COMMAND: /look
    #----------------------------------------------------------------------------------------------
    @discord.app_commands.command(name='look', description=DESCRIPTION)
    async def look(self, interaction: discord.Interaction):
        print(f"Received /look command from {interaction.user.display_name}")

        location = skale.get_player_location(interaction.user.id)

        # check whether user is logged in
        if not location or interaction.user.id not in user_accounts:
            embed = discord.Embed(title="No Account Detected", description=LOGIN_FIRST)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(description="`/look`\n" + Locations.location_descriptions[location])

        await interaction.response.send_message(embed=embed, ephemeral=True)
