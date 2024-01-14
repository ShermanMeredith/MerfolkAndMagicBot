from os import environ

import discord
from discord.ext import commands

from utils.accounts import user_accounts
from data.locations import Locations
import utils.database as database
import utils.skale as skale

# Config Variables
DESCRIPTION = "Heal your HP to full"
LOGIN_FIRST = f"""Looks like you aren't logged in right now...
Go to <#{database.get_login_channel_id(int(environ.get("GUILD_ID")))}> to sign up or log in, then try again"""


#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(HealCommand(bot))


#==================================================================================================
# HEAL COMMAND
#==================================================================================================
class HealCommand(commands.Cog, name="Heal Command"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #----------------------------------------------------------------------------------------------
    # COMMAND: /heal
    #----------------------------------------------------------------------------------------------
    @discord.app_commands.command(name='heal', description=DESCRIPTION)
    async def help(self, interaction: discord.Interaction):
        print(f"Received /heal command from {interaction.user.display_name}")

        # check whether user is logged in
        if interaction.user.id not in user_accounts:
            embed = discord.Embed(title="No Account Detected", description=LOGIN_FIRST)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        message = "`/heal`\n"

        player_location = skale.get_player_location(interaction.user.id)
        if player_location != Locations.CITY_CLINIC:
            message = "Can't heal here."
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        player_inventory = skale.get_player_inventory(interaction.user.id)
        message += f"Healing costs 5g.\nYou have {player_inventory.gold_balance}g."
        heal_embed = discord.Embed(description=message)
        await interaction.response.send_message(embed=heal_embed, view=HealView(), ephemeral=True)


#==================================================================================================
# HEAL VIEW
#==================================================================================================
class HealView(discord.ui.View):
    #----------------------------------------------------------------------------------------------
    # HEAL BUTTON
    #----------------------------------------------------------------------------------------------
    @discord.ui.button(label="<Heal>", style=discord.ButtonStyle.green, row=0)
    async def button_heal(self, interaction: discord.Interaction, button: discord.ui.Button):
        player_inventory = skale.get_player_inventory(interaction.user.id)
        player_stats = skale.get_player_stats(interaction.user.id)

        if player_inventory.gold_balance < 5:
            message = "You can't afford that."

        elif player_stats["current_hp"] >= player_stats["max_hp"]:
            message = "You are already fully healed."

        else:
            amount_healed = player_stats["max_hp"] - player_stats["current_hp"]
            message = (
                "The doctor heals you to full!\n`"
                f"{amount_healed} HP healed`\n`"
                "5g removed from your Inventory`"
            )

            player_inventory.gold_balance -= 5
            skale.set_player_inventory(interaction.user.id, player_inventory)

            player_stats["current_hp"] = player_stats["max_hp"]
            skale.set_player_stats(interaction.user.id, player_stats)

        await interaction.response.send_message(embed=discord.Embed(description=message), ephemeral=True)
