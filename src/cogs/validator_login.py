from os import environ
from typing import Dict

import discord
from discord.ext import commands, tasks

from utils.accounts import user_accounts


#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(LoginValidator(bot))


#==================================================================================================
# LOGIN VALIDATOR
#==================================================================================================
class LoginValidator(commands.Cog, name="LoginValidator"):
    VALIDATE_FREQUENCY = 1

    is_initialized = False
    is_validating_logged_in_users = False

    location_roles: Dict[int, discord.Role] = {}

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
            self.logged_in_role = self.guild.get_role(int(environ.get("LOGGED_IN_ROLE_ID")))

            self.is_initialized = True

        self.validate_logged_in_users.start()

    #----------------------------------------------------------------------------------------------
    # TASK: VALIDATE LOGGED IN USERS
    #----------------------------------------------------------------------------------------------
    @tasks.loop(minutes=VALIDATE_FREQUENCY)
    async def validate_logged_in_users(self):
        if self.is_validating_logged_in_users is True:
            return

        self.is_validating_logged_in_users = True

        to_add = [
            member for member in self.guild.members
            if member.id in user_accounts and self.logged_in_role not in member.roles
        ]

        for member in to_add:
            member_name = f"{member.display_name} ({member.id})"
            print(f"{member_name} - Adding {self.logged_in_role.name}")
            await member.add_roles(self.logged_in_role)

        to_remove = [
            member for member in self.guild.members
            if member.id not in user_accounts and self.logged_in_role in member.roles
        ]

        for member in to_remove:
            member_name = f"{member.display_name} ({member.id})"
            print(f"{member_name} - Removing {self.logged_in_role.name}")
            await member.remove_roles(self.logged_in_role)

        self.is_validating_logged_in_users = False
