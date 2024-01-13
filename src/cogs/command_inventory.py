from os import environ
from typing import List, Dict, Any

import discord
from discord.ext import commands

from data.items import Items, ItemType
from utils.accounts import user_accounts
import utils.database as database
import utils.skale as skale

# Config Variables
DESCRIPTION = "Purchase an item"
LOGIN_FIRST = f"""Looks like you aren't logged in right now...
Go to <#{database.get_login_channel_id(int(environ.get("GUILD_ID")))}> to sign up or log in, then try again"""


#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(InventoryCommand(bot))


#==================================================================================================
# INVENTORY COMMAND
#==================================================================================================
class InventoryCommand(commands.Cog, name="Inventory Command"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #----------------------------------------------------------------------------------------------
    # COMMAND: /inventory
    #----------------------------------------------------------------------------------------------
    @discord.app_commands.command(name='inventory', description=DESCRIPTION)
    async def inventory(self, interaction: discord.Interaction):
        print(f"Received /inventory command from {interaction.user.display_name}")

        # check whether user is logged in
        if interaction.user.id not in user_accounts:
            embed = discord.Embed(title="No Account Detected", description=LOGIN_FIRST)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        message = "`/inventory`\nYou look in your inventory and see:"

        inventory = skale.get_player_inventory(interaction.user.id)

        title = f"{str(inventory.gold_balance)}g"

        description = ""
        if len(inventory.items) > 0:
            description = ">>> "
            for item_id in inventory.items:
                if inventory.items[item_id] == 0:
                    continue
                description += f"{inventory.items[item_id]}x <{Items.item_names[item_id]}>"
                if Items.get_item_type(item_id) == ItemType.EQUIPPABLE:
                    description += " [can __equip__]"
                elif Items.get_item_type(item_id) == ItemType.EQUIPPED:
                    description += " [equipped. Can __unequip__]"
                description += "\n"

        embed = discord.Embed(title=title, description=description)

        await interaction.response.send_message(message, embed=embed, ephemeral=True)
