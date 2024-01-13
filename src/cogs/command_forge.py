from os import environ
from typing import List, Dict, Any

import discord
from discord.ext import commands

from utils.accounts import user_accounts
import utils.database as database
import utils.skale as skale
from data.locations import Locations
from data.items import Items, ItemType

# Config Variables
DESCRIPTION = "Forge something"
LOGIN_FIRST = f"""Looks like you aren't logged in right now...
Go to <#{database.get_login_channel_id(int(environ.get("GUILD_ID")))}> to sign up or log in, then try again"""


#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(ForgeCommand(bot))


#==================================================================================================
# FORGE COMMAND
#==================================================================================================
class ForgeCommand(commands.Cog, name="Forge Command"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #----------------------------------------------------------------------------------------------
    # COMMAND: /forge
    #----------------------------------------------------------------------------------------------
    @discord.app_commands.command(name='forge', description=DESCRIPTION)
    async def forge(self, interaction: discord.Interaction):
        print(f"Received /forge command from {interaction.user.display_name}")

        location = skale.get_player_location(interaction.user.id)

        # check whether user is logged in
        if not location or interaction.user.id not in user_accounts:
            embed = discord.Embed(title="No Account Detected", description=LOGIN_FIRST)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        message = "`/forge`\n"

        if location not in Locations.forge_items:
            message += "Can't forge here."
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        forge_items = Locations.forge_items[location]

        if len(forge_items) == 0:
            message += "You can't forge anything here now. Check again later."
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        player_inventory = skale.get_player_inventory(interaction.user.id)
        craftable_items = "Crafting materials:\n"
        for item in player_inventory.items:
            if player_inventory.items[item] > 0 and Items.get_item_type(item) == ItemType.INGREDIENT:
                craftable_items += f"{player_inventory.items[item]}x <{Items.item_names[item]}>\n"

        forge_embed = discord.Embed(
            title="What do you want to forge?",
            description=craftable_items
        )
        await interaction.response.send_message(embed=forge_embed, view=ForgeView(forge_items), ephemeral=True)


#==================================================================================================
# FORGE VIEW
#==================================================================================================
class ForgeView(discord.ui.View):
    def __init__(self, forge_items: List[Dict[str, Any]]):
        super().__init__()
        for i in range(len(forge_items)):
            self.add_item(ForgeItemButton(i, forge_items[i]))


#==================================================================================================
# FORGE ITEM BUTTON
#==================================================================================================
class ForgeItemButton(discord.ui.Button):
    #----------------------------------------------------------------------------------------------
    # INIT
    #----------------------------------------------------------------------------------------------
    def __init__(self, row: int, forge_items: Dict[str, Any]):
        self.ingredients: Dict[int, int] = forge_items["ingredients"]
        self.item_id = forge_items["id"]
        self.item_name = Items.item_names[self.item_id]

        ingredients = ""
        for item in self.ingredients:
            ingredients += f" — {self.ingredients[item]}x <{Items.item_names[item]}>"

        button_label = f"<{self.item_name}> {ingredients}"

        super().__init__(
            style=discord.ButtonStyle.blurple,
            label=button_label,
            row=row
        )

    #----------------------------------------------------------------------------------------------
    # CALLBACK
    #----------------------------------------------------------------------------------------------
    async def callback(self, interaction: discord.Interaction):
        message = f"`/forge {self.item_name}`\n"
        player_inventory = skale.get_player_inventory(interaction.user.id)
        response = "Kate says, \"You got it!\"\n"
        for item in self.ingredients:
            if player_inventory.items[item] >= self.ingredients[item]:
                player_inventory.items[item] -= self.ingredients[item]
                response += f"`{self.ingredients[item]} <{Items.item_names[item]}> removed from inventory`\n"
            else:
                message += "You don't have the necessary materials to forge that."
                embed = discord.Embed(description=message)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

        response += "Kate hammers away at the anvil and hands you the item.\n"
        response += f"`1 <{self.item_name}> added to inventory.`"

        player_inventory.items[self.item_id] += 1
        skale.set_player_inventory(interaction.user.id, player_inventory)

        embed = discord.Embed(description=message + response)
        await interaction.response.send_message(embed=embed, ephemeral=True)
