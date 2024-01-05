from os import environ
from io import StringIO
import discord
from eth_account.signers.local import LocalAccount
from eth_account import Account
from eth_keys.exceptions import ValidationError
from utils.accounts import user_accounts

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

#==================================================================================================
# ACCOUNT MANAGEMENT VIEW
#==================================================================================================
class AccountManagementView(discord.ui.View):

    PASSPHRASE = environ.get("SEEDPHRASE_PASSPHRASE")

    account_manager = Account()
    account_manager.enable_unaudited_hdwallet_features()

    #----------------------------------------------------------------------------------------------
    # INIT
    #----------------------------------------------------------------------------------------------
    def __init__(self):
        super().__init__(timeout=None)

    #----------------------------------------------------------------------------------------------
    # SIGN UP BUTTON
    #----------------------------------------------------------------------------------------------
    @discord.ui.button(
        label="Sign Up",
        style=discord.ButtonStyle.green,
        row=0,
        custom_id="account-management:sign-up-button"
    )
    async def button_sign_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in user_accounts:
            # user already logged in
            already_logged_in = discord.Embed(
                title="Already Logged In",
                description="You are already logged in to an account"
            )
            await interaction.response.send_message(embed=already_logged_in, ephemeral=True)
            return

        # create new account
        (user_account, seedphrase) = self.account_manager.create_with_mnemonic(
            passphrase=self.PASSPHRASE
        )

        # save account in user accounts dictionary
        user_accounts[interaction.user.id] = user_account

        # TODO: initialize new account on Nebula

        # send interaction response
        seedphrase_file = discord.File(fp=StringIO(seedphrase), filename="RecoveryPhrase.txt")
        signup_embed = discord.Embed(title="Signup Success", description=SIGNUP_MESSAGE)

        await interaction.response.send_message(
            embed=signup_embed,
            file=seedphrase_file,
            ephemeral=True
        )

    #----------------------------------------------------------------------------------------------
    # LOG IN BUTTON
    #----------------------------------------------------------------------------------------------
    @discord.ui.button(
        label="Log In",
        style=discord.ButtonStyle.blurple,
        row=1,
        custom_id="account-management:log-in-button"
    )
    async def button_log_in(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(LogInModal(self.PASSPHRASE, self.account_manager))

    #----------------------------------------------------------------------------------------------
    # LOG OUT BUTTON
    #----------------------------------------------------------------------------------------------
    @discord.ui.button(
        label="Log Out",
        style=discord.ButtonStyle.red,
        row=1,
        custom_id="account-management:log-out-button"
    )
    async def button_log_out(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"Received Account Logout Command from {interaction.user.display_name}")

        if interaction.user.id not in user_accounts:
            # user was not signed in
            logout_embed = discord.Embed(title="Already Logged Out")
            await interaction.response.send_message(embed=logout_embed, ephemeral=True)
            return

        # remove user from user accounts dictionary
        user_accounts.pop(interaction.user.id)

        # send response
        logout_embed = discord.Embed(title="You Are Now Logged Out")
        await interaction.response.send_message(embed=logout_embed, ephemeral=True)


#==================================================================================================
# LOG IN MODAL
#==================================================================================================
class LogInModal(discord.ui.Modal, title="Enter Recovery Phrase"):

    recovery_phrase = discord.ui.TextInput(
        label="Recovery Phrase",
        style=discord.TextStyle.short,
        placeholder="12-Word Seed Phrase",
    )

    #----------------------------------------------------------------------------------------------
    # INIT
    #----------------------------------------------------------------------------------------------
    def __init__(self, passphrase: str, account_manager: Account):
        self.passphrase = passphrase
        self.account_manager = account_manager
        super().__init__()

    #----------------------------------------------------------------------------------------------
    # ON SUBMIT
    #----------------------------------------------------------------------------------------------
    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_account: LocalAccount = self.account_manager.from_mnemonic(
                mnemonic=self.recovery_phrase.value,
                passphrase=self.passphrase
            )
            print("got user account")
        except ValidationError as e:
            print(f"Seedphrase Validation Failed")
            # send user the error message
            embed = discord.Embed(title="Login Error", description=e)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        print(f"Seedphrase Validation Success")

        # store account in user accounts dictionary
        user_accounts[interaction.user.id] = user_account

        # send response
        await interaction.response.send_message(
            embed=discord.Embed(title="Login Success"),
            ephemeral=True
        )
