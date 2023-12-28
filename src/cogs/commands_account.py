# builtin modules
from os import environ
from io import StringIO

# installed modules
from discord import app_commands, Embed, Attachment, File, Interaction
from discord.ext import commands
from eth_account.signers.local import LocalAccount
from eth_account import Account
from eth_keys.exceptions import ValidationError

# local modules
from utils.accounts import user_accounts

# Config Variables
ACCOUNT_GROUP_DESCRIPTION = "Commands related to user accounts"
LOGIN_WITH_PHRASE_DESCRIPTION = "Log in to your account using your recovery phrase"
SEEDPHRASE_FILE_DESCRIPTION = "The file containing your seedphrase. This was created when you signed up."
SIGNUP_MESSAGE = """Your new account has been created, and you are now logged in!

When you are ready to continue, type /start to start your adventure!

>>> **IMPORTANT:**
>>> Download and save your recovery phrase!!! <<<
The recovery phrase for this account is attached to this message.
You will occasionally need it to log back in.

**WARNING:**
We do not store your recovery phrase; it is your responsibility to keep it safe and not to lose it.
Never share this recovery phrase with anyone else.
Our team members will never ever ask you for your recovery phrase.
Only trust this bot with the recovery phrase."""


#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(AccountCog(bot))


#==================================================================================================
# ACCOUNT COG
#==================================================================================================
class AccountCog(commands.Cog, name="Login Cog"):

    PASSPHRASE = environ.get("SEEDPHRASE_PASSPHRASE")

    account_manager = Account()
    account_manager.enable_unaudited_hdwallet_features()

    group_account = app_commands.Group(name="account", description=ACCOUNT_GROUP_DESCRIPTION)

    #----------------------------------------------------------------------------------------------
    # INIT
    #----------------------------------------------------------------------------------------------
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #----------------------------------------------------------------------------------------------
    # COMMAND: /signup
    #----------------------------------------------------------------------------------------------
    @group_account.command(name='signup', description="Create a new account")
    async def signup(self, interaction: Interaction):
        print(f"Received Account Signup Command from {interaction.user.display_name}")

        if interaction.user.id in user_accounts:
            # user already logged in
            await interaction.response.send_message(
                embed=Embed(
                    title="Already Logged In",
                    description="You are already logged in to an account"
                ),
                ephemeral=True
            )
            return

        # create new account
        (user_account, seedphrase) = self.account_manager.create_with_mnemonic(
            passphrase=self.PASSPHRASE
        )

        # save account in user accounts dictionary
        user_accounts[interaction.user.id] = user_account

        # TODO: initialize new account on Nebula

        # send interaction response
        seedphrase_file = File(fp=StringIO(seedphrase), filename="RecoveryPhrase.txt")
        signup_embed = Embed(title="Signup Success", description=SIGNUP_MESSAGE)

        await interaction.response.send_message(
            embed=signup_embed,
            file=seedphrase_file,
            ephemeral=True
        )

    #----------------------------------------------------------------------------------------------
    # COMMAND: /logout
    #----------------------------------------------------------------------------------------------
    @group_account.command(name='logout', description="Log out of your account")
    async def logout(self, interaction: Interaction):
        print(f"Received Account Logout Command from {interaction.user.display_name}")

        if interaction.user.id not in user_accounts:
            # user was not signed in
            logout_embed = Embed(title="Already Logged Out")
            await interaction.response.send_message(embed=logout_embed, ephemeral=True)
            return

        # remove user from user accounts dictionary
        user_accounts.pop(interaction.user.id)

        # send response
        logout_embed = Embed(title="You Are Now Logged Out")
        await interaction.response.send_message(embed=logout_embed, ephemeral=True)

    #----------------------------------------------------------------------------------------------
    # COMMAND: /login + file - Doesn't work yet
    #----------------------------------------------------------------------------------------------
    #@group_account.command(name='login', description="Log in to your account")
    #@app_commands.describe(recovery_phrase_file=SEEDPHRASE_FILE_DESCRIPTION)
    #async def login(self, interaction: Interaction, recovery_phrase_file: Attachment):
        #print(f"Received Account Login Command from {interaction.user.display_name}")

        #seedphrase_file = await recovery_phrase_file.to_file()
        #with open(seedphrase_file) as f:
            #seedphrase = f.read()

        #await self.process_seedphrase(seedphrase)

    #----------------------------------------------------------------------------------------------
    # COMMAND: /login + seedphrase
    #----------------------------------------------------------------------------------------------
    @group_account.command(name='login-phrase', description=LOGIN_WITH_PHRASE_DESCRIPTION)
    async def login_phrase(self, interaction: Interaction, recovery_phrase: str):
        print(f"Received Account Login Command from {interaction.user.display_name}")
        await self.process_seedphrase(interaction, recovery_phrase)

    #----------------------------------------------------------------------------------------------
    # PROCESS SEEDPHRASE
    #----------------------------------------------------------------------------------------------
    async def process_seedphrase(self, interaction: Interaction, seedphrase: str):
        # get account from seedphrase
        try:
            user_account: LocalAccount = self.account_manager.from_mnemonic(
                mnemonic=seedphrase,
                passphrase=self.PASSPHRASE
            )
        except ValidationError as e:
            print(f"Seedphrase Validation Failed")
            # send user the error message
            embed = Embed(title="Login Error", description=e)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        print(f"Seedphrase Validation Success")

        # store account in user accounts dictionary
        user_accounts[interaction.user.id] = user_account

        # send response
        await interaction.response.send_message(
            embed=Embed(title="Login Success"),
            ephemeral=True
        )
