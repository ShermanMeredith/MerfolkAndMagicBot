from os import environ

import discord
from discord.ext import commands

from utils.accounts import user_accounts
import utils.database as database
import utils.skale as skale
from data.locations import Locations
from data.items import Items

# Config Variables
DESCRIPTION = "Mine some ore"
LOGIN_FIRST = f"""Looks like you aren't logged in right now...
Go to <#{database.get_login_channel_id(int(environ.get("GUILD_ID")))}> to sign up or log in, then try again"""


#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(MineCommand(bot))


#==================================================================================================
# MINE COMMAND
#==================================================================================================
class MineCommand(commands.Cog, name="Mine Command"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #----------------------------------------------------------------------------------------------
    # COMMAND: /mine
    #----------------------------------------------------------------------------------------------
    @discord.app_commands.command(name='mine', description=DESCRIPTION)
    async def mine(self, interaction: discord.Interaction):
        print(f"Received /mine command from {interaction.user.display_name}")

        location = skale.get_player_location(interaction.user.id)

        # check whether user is logged in
        if not location or interaction.user.id not in user_accounts:
            embed = discord.Embed(title="No Account Detected", description=LOGIN_FIRST)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        message = "`/mine`\n"

        if location not in Locations.location_has_copper or not Locations.location_has_copper[location]:
            message += "Nothing to mine here."
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        player_inventory = skale.get_player_inventory(interaction.user.id)
        player_inventory.items[Items.COPPER_ORE] += 1
        skale.set_player_inventory(interaction.user.id, player_inventory)

        message += "You mine the Copper.\n`1 <Copper Ore> added to inventory`"
        embed = discord.Embed(description=message)

        await interaction.response.send_message(embed=embed, ephemeral=True)
