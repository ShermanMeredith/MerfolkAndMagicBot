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
from cogs.command_go import GoCommand
from utils.skale import Inventory

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

        player_inventory = skale.get_player_inventory(interaction.user.id)
        player_stats = skale.get_player_stats(interaction.user.id)

        if location == Locations.CITY_BLACKSMITH:
            message += "You go to attack Kate the Blacksmith, but she easily kicks your ass."
            embeds = [discord.Embed(description=message)]
            message = "You collapse."
            await self.die(message, interaction, player_inventory, player_stats, embeds)
            await interaction.response.send_message(embeds=embeds, ephemeral=True)
            return

        elif location == Locations.CITY_ALCHEMIST:
            message += "You go to attack the Alchemist, but he easily kicks your ass."
            embeds = [discord.Embed(description=message)]
            message = "You collapse."
            await self.die(message, interaction, player_inventory, player_stats, embeds)
            await interaction.response.send_message(embeds=embeds, ephemeral=True)
            return

        elif location == Locations.CITY_MAGE_TOWER:
            message += "You go to attack the Mage, but he easily kicks your ass."
            embeds = [discord.Embed(description=message)]
            message = "You collapse."
            await self.die(message, interaction, player_inventory, player_stats, embeds)
            await interaction.response.send_message(embeds=embeds, ephemeral=True)
            return

        elif location == Locations.CITY_CLINIC:
            message += "You go to attack the Doctor, but he easily kicks your ass."
            embeds = [discord.Embed(description=message)]
            message = "You collapse."
            await self.die(message, interaction, player_inventory, player_stats, embeds)
            await interaction.response.send_message(embeds=embeds, ephemeral=True)
            return

        elif location == Locations.MOUNTAIN_B4:
            await interaction.response.defer(ephemeral=True, thinking=True)

            is_sword_equipped = player_inventory.items[Items.COPPER_SWORD_EQUIPPED] > 0
            if is_sword_equipped:
                attack_action = "swing your <Copper Sword> at"
                attack_damage = player_stats["base_attack"] + 5
            else:
                attack_action = "punch"
                attack_damage = player_stats["base_attack"]

            skeleton_hp = 10

            message += (
                "\nYou begin an attack against <Skeleton>\n\n"
                "`Skeleton LVL 1: 10/10 HP | 2 ATK | 1 DEF | 8 SPD`\n"
                f"`You: {player_stats['current_hp']}/{player_stats['max_hp']} HP | {attack_damage} ATK | {player_stats['base_defense']} DEF | {player_stats['base_speed']} SPD`\n\n"
                "You attack first!"
            )
            embeds = [discord.Embed(description=message)]
            round = 1
            while skeleton_hp > 0 and player_stats["current_hp"] > 0:
                message = f"You {attack_action} <Skeleton>.\n"

                damage = random.randint(attack_damage, attack_damage + 2)
                skeleton_hp -= damage
                message = f"You {attack_action} <Skeleton>.\n`<Skeleton> loses {damage} HP`\n\n"

                damage = random.randint(1,3)
                player_stats["current_hp"] -= damage
                message += f"<Skeleton> punches you.\n`You lose {damage} HP`"

                embeds.append(discord.Embed(title=f"Round {round}", description=message))
                round += 1

            if player_stats["current_hp"] > 0:
                message = (
                    "<Skeleton> dies.\n"
                    "<Skeleton> drops 3g and 1 <Copper Ore>.\n"
                    f"`3g added to inventory.`\n"
                    f"`1 <Copper Ore> added to inventory.`"
                )
                embeds.append(discord.Embed(description=message))
                player_inventory.gold_balance += 3
                player_inventory.items[Items.COPPER_ORE] += 1
            else:
                message = "You collapse."

                copper_lost = min(player_inventory.items[Items.COPPER_ORE], 3)
                if copper_lost > 0:
                    if copper_lost > 1:
                        message += f"\n`{copper_lost} <Copper Ore> dropped from inventory`"
                    else:
                        message += "\n`<Copper Ore> dropped from inventory`"
                    player_inventory.items[Items.COPPER_ORE] -= copper_lost

                if is_sword_equipped:
                    message += "\n`<Copper Sword> dropped.`"
                    player_inventory.items[Items.COPPER_SWORD_EQUIPPED] -= 1

                await self.die(message, interaction, player_inventory, player_stats, embeds)

            skale.set_player_inventory(interaction.user.id, player_inventory)
            skale.set_player_stats(interaction.user.id, player_stats)
            await interaction.followup.send(embeds=embeds, ephemeral=True)


    async def die(self, message: str, interaction: discord.Interaction, player_inventory: Inventory, player_stats: Dict[str, int], embeds: List[discord.Embed]):
        amount_pilfered = int(player_inventory.gold_balance / 2)
        message += (
            "\n\nYour body is discovered by a group of adventurers.\n"
            "They bring you to the doctor in Mara.\n"
            f"`{player_stats['max_hp']} HP healed`\n\n"
            "Doctor says, \"Quite a hit you took there. I'll take half your gold for healing you.\"\n"
            f"`{amount_pilfered}g pilfered from your Inventory.`\n\n"
            "Doctor says, \"Come again soon!\""
        )
        embeds.append(discord.Embed(description=message))
        player_stats["current_hp"] = player_stats["max_hp"]
        player_inventory.gold_balance -= amount_pilfered

        go_cog: GoCommand = self.bot.get_cog("Go Command")
        await go_cog.set_new_roles(interaction, Locations.Region.MOUNTAIN, Locations.Region.CITY)
        await go_cog.set_channel_permissions(
            interaction,
            skale.get_previous_location(interaction.user.id),
            skale.get_player_location(interaction.user.id),
            Locations.CITY_CLINIC
        )
        skale.set_player_location(interaction.user.id, Locations.CITY_CLINIC)

        new_channel = interaction.guild.get_channel(Locations.location_channel_ids[Locations.CITY_CLINIC])
        message = f"You find yourself {Locations.location_names[Locations.CITY_CLINIC]}:\n{new_channel.mention}"
        embeds.append(discord.Embed(description=message))
