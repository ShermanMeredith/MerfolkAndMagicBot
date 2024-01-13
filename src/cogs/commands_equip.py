from os import environ

import discord
from discord.ext import commands

from data.items import Items, ItemType
from utils.accounts import user_accounts
import utils.database as database
import utils.skale as skale

# Config Variables
DESCRIPTION_EQUIP = "Equip an equippable item"
DESCRIPTION_UNEQUIP = "Unequip an equippable item"
LOGIN_FIRST = f"""Looks like you aren't logged in right now...
Go to <#{database.get_login_channel_id(int(environ.get("GUILD_ID")))}> to sign up or log in, then try again"""


#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(EquipCommands(bot))


#==================================================================================================
# EQUIP COMMANDS
#==================================================================================================
class EquipCommands(commands.Cog, name="Equip Commands"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #----------------------------------------------------------------------------------------------
    # COMMAND: /equip
    #----------------------------------------------------------------------------------------------
    @discord.app_commands.command(name='equip', description=DESCRIPTION_EQUIP)
    @discord.app_commands.describe(item_name="Name of the item you want to equip")
    async def equip(self, interaction: discord.Interaction, item_name: str):
        print(f"Received /equip command from {interaction.user.display_name}")

        # check whether user is logged in
        if interaction.user.id not in user_accounts:
            embed = discord.Embed(title="No Account Detected", description=LOGIN_FIRST)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        message = f"`/equip {item_name}`\n"

        # check that item_name is valid
        item_name = item_name.lower()
        valid_item_names = [name.lower() for name in Items.item_names.values()]
        if item_name not in valid_item_names:
            message += "Invalid item name."
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        item_id = 0
        for item in Items.item_names.items():
            if item_name == item[1].lower() and Items.get_item_type(item[0]) == ItemType.EQUIPPABLE:
                item_id = item[0]
                item_name = item[1]

        if item_id == 0:
            message += f"<{item_name}> is not equippable."
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        player_inventory = skale.get_player_inventory(interaction.user.id)
        if player_inventory.items[item_id] == 0:
            message += f"You don't have a <{item_name}>."
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # unequip any existing equipped items
        equipped_items = [
            item for item in player_inventory.items
            if player_inventory.items[item] > 0
            and Items.get_item_type(item) == ItemType.EQUIPPED
        ]
        for item in equipped_items:
            message += f"You unequip your <{Items.item_names[item]}>\n"
            number_equipped = player_inventory.items[item]
            player_inventory.items[item] = 0
            player_inventory.items[Items.get_unequipped_version(item)] += number_equipped

        # swap the unequipped item with an equipped item
        equipped_version = Items.get_equipped_version(item_id)

        player_inventory.items[item_id] -= 1
        player_inventory.items[equipped_version] += 1
        skale.set_player_inventory(interaction.user.id, player_inventory)

        message += f"You equip your <{item_name}>."
        embed = discord.Embed(description=message)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    #----------------------------------------------------------------------------------------------
    # COMMAND: /unequip
    #----------------------------------------------------------------------------------------------
    @discord.app_commands.command(name='unequip', description=DESCRIPTION_EQUIP)
    @discord.app_commands.describe(item_name="Name of the item you want to unequip")
    async def unequip(self, interaction: discord.Interaction, item_name: str):
        print(f"Received /unequip command from {interaction.user.display_name}")

        # check whether user is logged in
        if interaction.user.id not in user_accounts:
            embed = discord.Embed(title="No Account Detected", description=LOGIN_FIRST)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        message = f"`/unequip {item_name}`\n"

        # check that item_name is valid
        item_name = item_name.lower()
        valid_item_names = [name.lower() for name in Items.item_names.values()]
        if item_name not in valid_item_names:
            message += "Invalid item name."
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        item_id = 0
        for item in Items.item_names.items():
            if item[1].lower() == item_name and Items.get_item_type(item[0]) == ItemType.EQUIPPED:
                item_id = item[0]
                item_name = item[1]

        if item_id == 0:
            message += f"<{item_name}> is not equippable."
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        player_inventory = skale.get_player_inventory(interaction.user.id)
        if player_inventory.items[item_id] == 0:
            message += f"You don't have a <{item_name}> equipped."
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # swap the unequipped item with an equipped item
        unequipped_version = Items.get_unequipped_version(item_id)
        number_equipped = player_inventory.items[item_id]
        player_inventory.items[item_id] = 0
        player_inventory.items[unequipped_version] += number_equipped
        skale.set_player_inventory(interaction.user.id, player_inventory)

        message += f"You unequip your <{item_name}>."
        embed = discord.Embed(description=message)
        await interaction.response.send_message(embed=embed, ephemeral=True)
