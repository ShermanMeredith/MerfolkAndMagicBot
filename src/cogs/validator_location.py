from os import environ
from typing import Dict

import discord
from discord.ext import commands, tasks

import utils.database as database
import utils.skale as skale
from utils.accounts import user_accounts
from data.locations import Locations


#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(LocationValidator(bot))


#==================================================================================================
# LOCATION VALIDATOR
#==================================================================================================
class LocationValidator(commands.Cog, name="Location Validator"):
    VALIDATE_FREQUENCY = 1

    is_initialized = False
    is_validating_logged_in_users = False
    is_validating_locations = False

    region_roles: Dict[int, discord.Role] = {}

    #----------------------------------------------------------------------------------------------
    # INIT
    #----------------------------------------------------------------------------------------------
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #----------------------------------------------------------------------------------------------
    # EVENT: ON READY
    #----------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.is_initialized:
            self.guild = self.bot.get_guild(int(environ.get("GUILD_ID")))

            for location in Locations.location_names:
                region = Locations.get_region(location)
                self.region_roles[location] = self.guild.get_role(Locations.region_role_ids[region])

            self.is_initialized = True

        self.validate_locations.start()

    #----------------------------------------------------------------------------------------------
    # TASK: VALIDATE USER LOCATIONS
    #----------------------------------------------------------------------------------------------
    @tasks.loop(minutes=VALIDATE_FREQUENCY)
    async def validate_locations(self):
        if self.is_validating_locations is True:
            return

        self.is_validating_locations = True

        for member_id in user_accounts:
            member = self.guild.get_member(member_id)
            if not member:
                continue

            member_name = f"{member.display_name} ({member.id})"

            player_location_id = skale.get_player_location(member_id)
            if not player_location_id:
                return

            region_role = self.region_roles[player_location_id]
            player_region_roles = [
                role for role in member.roles
                if role in self.region_roles.values()
                and role != region_role
            ]

            if player_region_roles:
                for role in player_region_roles:
                    print(f"{member_name} - Removing {role.name}")
                await member.remove_roles(player_region_roles)

            if region_role not in member.roles:
                print(f"{member_name} - Adding {region_role.name}")
                await member.add_roles(region_role)

        self.is_validating_locations = False
