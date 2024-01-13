import random
from os import environ
from typing import List, Dict, Any

import discord
from discord.ext import commands

from data.items import Items
from utils.accounts import user_accounts
import utils.database as database
import utils.skale as skale
from data.locations import Locations

# Config Variables
DESCRIPTION = "Attack an enemy"
TARGET_DESCRIPTION = "What do you want to attack?"
LOGIN_FIRST = f"""Looks like you aren't logged in right now...
Go to <#{database.get_login_channel_id(int(environ.get("GUILD_ID")))}> to sign up or log in, then try again"""


attack_targets: Dict[int, List[str]] = {
    Locations.CITY_ALCHEMIST: ["alchemist", "potion seller", "shopkeeper"],
    Locations.CITY_BLACKSMITH: ["kate", "blacksmith", "shopkeeper"],
    Locations.CITY_CLINIC: ["doctor"],
    Locations.CITY_MAGE_TOWER: ["mage", "wizard", "sorcerer"],
    Locations.MOUNTAIN_B1: [],
    Locations.MOUNTAIN_B2: [],
    Locations.MOUNTAIN_B4: ["skeleton"]
}


#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(AttackCommand(bot))


#==================================================================================================
# ATTACK COMMAND
#==================================================================================================
class AttackCommand(commands.Cog, name="Attack Command"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #----------------------------------------------------------------------------------------------
    # COMMAND: /attack
    #----------------------------------------------------------------------------------------------
    @discord.app_commands.command(name='attack', description=DESCRIPTION)
    @discord.app_commands.describe(target=TARGET_DESCRIPTION)
    async def attack(self, interaction: discord.Interaction, target: str):
        print(f"Received /attack {target} command from {interaction.user.display_name}")

        location = skale.get_player_location(interaction.user.id)

        # check whether user is logged in
        if not location or interaction.user.id not in user_accounts:
            embed = discord.Embed(title="No Account Detected", description=LOGIN_FIRST)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        message = f"`/attack {target}`\n"

        if location not in attack_targets:
            embed = discord.Embed(description=message + "Can't attack anything here.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
 
        if len(attack_targets[location]) == 0:
            message += "You don't see anything you can attack here. Check again later."
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if target not in attack_targets[location]:
            embed = discord.Embed(description=message + f"There is no {target} to attack.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if location == Locations.CITY_BLACKSMITH:
            message += "You go to attack Kate the Blacksmith, but she easily kicks your ass.\n`You are dead`"
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        elif location == Locations.CITY_ALCHEMIST:
            message += "You go to attack the Alchemist, but he easily kicks your ass.\n`You are dead`"
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        elif location == Locations.CITY_MAGE_TOWER:
            message += "You go to attack the Mage, but he easily kicks your ass.\n`You are dead`"
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        elif location == Locations.CITY_CLINIC:
            message += "You go to attack the Doctor, but he easily kicks your ass.\n`You are dead`"
            embed = discord.Embed(description=message)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        elif location == Locations.MOUNTAIN_B4:
            await interaction.response.defer(ephemeral=True, thinking=True)

            player_inventory = skale.get_player_inventory(interaction.user.id)
            is_sword_equipped = player_inventory.items[Items.COPPER_SWORD_EQUIPPED] > 0
            if is_sword_equipped:
                attack_action = "swing your <Copper Sword> at"
                attack_damage = (5, 7)
            else:
                attack_action = "punch"
                attack_damage = (1, 3)

            skeleton_hp = 10
            player_hp = 20

            message += (
                "\nYou begin an attack against <Skeleton>\n\n"
                "`Skeleton LVL 1: 10/10 HP | 2 ATK | 1 DEF | 8 SPD`\n"
                f"`You: {player_hp}/20 HP | {attack_damage[0]} ATK | 1 DEF | 13 SPD`\n\n"
                "You attack first!"
            )
            embeds = [discord.Embed(description=message)]
            round = 1
            while skeleton_hp > 0 and player_hp > 0:
                message = f"You {attack_action} <Skeleton>.\n"

                damage = random.randint(attack_damage[0], attack_damage[1])
                skeleton_hp -= damage
                message = f"You {attack_action} <Skeleton>.\n`<Skeleton> loses {damage} HP`\n\n"

                damage = random.randint(1,3)
                player_hp -= damage
                message += f"<Skeleton> punches you.\n`You lose {damage} HP`"

                embeds.append(discord.Embed(title=f"Round {round}", description=message))
                round += 1

            if player_hp > 0:
                message = (
                    "<Skeleton> dies.\n"
                    "<Skeleton> drops 3g.\n"
                    f"`3g added to inventory.`\n"
                    "<Skeleton> drops 1 <Copper Ore>.\n"
                    f"`1 <Copper Ore> added to inventory.`"
                )
                embeds.append(discord.Embed(description=message))
                player_inventory.gold_balance += 3
                player_inventory.items[Items.COPPER_ORE] += 1
            else:
                message = "You collapse.\n`"

                copper_lost = min(player_inventory.items[Items.COPPER_ORE], 3)
                if copper_lost > 0:
                    if copper_lost > 1:
                        message += f"{copper_lost} "
                    message += "<Copper Ore> dropped from inventory`"
                    player_inventory.items[Items.COPPER_ORE] -= copper_lost
                
                if is_sword_equipped:
                    message += "\n`<Copper Sword> dropped.`"
                    player_inventory.items[Items.COPPER_SWORD_EQUIPPED] -= 1
                embeds.append(discord.Embed(description=message))

                amount_pilfered = int(player_inventory.gold_balance / 2)
                message = (
                    "Your body is discovered by a group of adventurers. They bring you to the doctor in Mara."
                    "Doctor says, \"Quite a hit you took there. I'll take half your gold for healing you.\""
                    f"`{amount_pilfered}g pilfered from your Inventory.`"
                    "Doctor says, \"Come again soon!\""
                )
                embeds.append(discord.Embed(description=message))
                player_inventory.gold_balance -= amount_pilfered

            skale.set_player_inventory(interaction.user.id, player_inventory)
            await interaction.followup.send(embeds=embeds, ephemeral=True)
