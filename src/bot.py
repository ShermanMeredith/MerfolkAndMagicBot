from asyncio import run
from os import environ

import discord
from discord.ext import commands


#==============================================================================
# BOT CONFIGURATION
#==============================================================================
class MerfolkAndMagicBot(commands.Bot):
    #--------------------------------------------------------------------------
    # INIT
    #--------------------------------------------------------------------------
    def __init__(self):
        intents = discord.Intents.none()

        self.initial_extensions = [
            "cogs.commands_account",
            #"cogs.command_go",
        ]

        super().__init__(
            command_prefix='!',
            intents = intents
        )

    #--------------------------------------------------------------------------
    # SETUP HOOK
    #--------------------------------------------------------------------------
    async def setup_hook(self):
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
    for guild in bot.guilds:
        print(f"Connected to {guild.name}")
    await bot.tree.sync()

async def main():
    token = environ.get("BOT_TOKEN")
    await bot.start(token)

if __name__ == "__main__":
    run(main())
