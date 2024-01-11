from asyncio import run
from os import environ

import discord
from discord.ext import commands

from login_panel import AccountManagementView


#==============================================================================
# BOT CONFIGURATION
#==============================================================================
class MerfolkAndMagicBot(commands.Bot):
    #--------------------------------------------------------------------------
    # INIT
    #--------------------------------------------------------------------------
    def __init__(self):
        intents = discord.Intents.none()
        # required to see emoji reactions
        intents.guild_reactions = True
        # required for checking message content
        intents.guild_messages = True
        intents.message_content = True
        # required for keeping guild members cache up to date
        intents.members = True
        # required for on guild join event
        # required for channel creation events for auto-message writing
        intents.guilds = True

        self.initial_extensions = [
            "cogs.command_go",
            "cogs.command_help",
            "cogs.commands_admin",
            "cogs.validator_location",
            "cogs.validator_login"
        ]

        super().__init__(
            command_prefix='!',
            intents = intents
        )

    #--------------------------------------------------------------------------
    # SETUP HOOK
    #--------------------------------------------------------------------------
    async def setup_hook(self):
        self.add_view(AccountManagementView(self))
        for extension in self.initial_extensions:
            await self.load_extension(extension)

    #--------------------------------------------------------------------------
    # CLOSE
    #--------------------------------------------------------------------------
    async def close(self):
        await super().close()


bot = MerfolkAndMagicBot()

@bot.event
async def on_ready():
    await bot.tree.sync()
    for guild in bot.guilds:
        print(f"Connected to {guild.name}")

async def main():
    token = environ.get("BOT_TOKEN")
    await bot.start(token)

if __name__ == "__main__":
    run(main())
