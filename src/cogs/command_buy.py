from os import environ
from typing import List, Dict, Any

import discord
from discord.ext import commands

from data.items import Items
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
    await bot.add_cog(BuyCommand(bot))


#==================================================================================================
# BUY COMMAND
#==================================================================================================
class BuyCommand(commands.Cog, name="Buy Command"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #----------------------------------------------------------------------------------------------
    # COMMAND: /buy
    #----------------------------------------------------------------------------------------------
    @discord.app_commands.command(name='buy', description=DESCRIPTION)
    async def buy(self, interaction: discord.Interaction):
        print(f"Received /buy command from {interaction.user.display_name}")

        location = skale.get_player_location(interaction.user.id)

        # check whether user is logged in
        if not location or interaction.user.id not in user_accounts:
            embed = discord.Embed(title="No Account Detected", description=LOGIN_FIRST)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        player_inventory = skale.get_player_inventory(interaction.user.id)
        shop_items = skale.get_shop_items(location)

        if shop_items is None:
            embed = discord.Embed(description="Can't buy anything here.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif len(shop_items) == 0:
            embed = discord.Embed(description="You don't see anything you can buy here. Check again later.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            buy_embed = discord.Embed(
                title="What do you want to buy?",
                description=f"You have {player_inventory.gold_balance}g"
            )
            await interaction.response.send_message(embed=buy_embed, view=BuyView(shop_items), ephemeral=True)


#==================================================================================================
# BUY VIEW
#==================================================================================================
class BuyView(discord.ui.View):
    def __init__(self, shop_items: List[Dict[str, Any]]):
        super().__init__()
        for i in range(len(shop_items)):
            self.add_item(ShopItemButton(i, shop_items[i]))


#==================================================================================================
# SHOP ITEM BUTTON
#==================================================================================================
class ShopItemButton(discord.ui.Button):
    #----------------------------------------------------------------------------------------------
    # INIT
    #----------------------------------------------------------------------------------------------
    def __init__(self, row: int, shop_item: Dict[str, Any]):
        self.price = shop_item["price"]
        self.item_id = shop_item["id"]
        self.item_name = Items.item_names[self.item_id]

        button_label = f"<{self.item_name}> — {self.price}g"

        super().__init__(
            style=discord.ButtonStyle.blurple,
            label=button_label,
            row=row
        )

    #----------------------------------------------------------------------------------------------
    # CALLBACK
    #----------------------------------------------------------------------------------------------
    async def callback(self, interaction: discord.Interaction):
        message = f"`/buy {self.item_name}`\n"
        player_inventory = skale.get_player_inventory(interaction.user.id)
        if player_inventory.gold_balance >= self.price:
            player_inventory.gold_balance -= self.price
            if self.price >= 0:
                player_inventory.items[self.item_id] += 1
            message += f"You bought <{self.item_name}>!"
            skale.set_player_inventory(interaction.user.id, player_inventory)
        else:
            message += "You can't afford that."

        embed = discord.Embed(description=message)
        await interaction.response.send_message(embed=embed, ephemeral=True)
