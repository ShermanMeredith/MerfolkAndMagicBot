from typing import Optional

import discord
from discord.ext import commands

import utils.skale as skale
from data.locations import Locations

# Config Variables
DESCRIPTION = "Leave this room and enter another room"
DIRECTION_DESCRIPTION = "Where do you want to go?"

CITY_OUTSIDE_DIRECTIONS = set(["gates", "gate", "entrance"])
CITY_SQUARE_DIRECTIONS = set(["mara", "out", "outside", "city"])
CITY_BLACKSMITH_DIRECTIONS = set(["blacksmith", "smith", "smithy", "armor shop", "sword shop",
                                  "item shop", "equipment shop"])
CITY_CLINIC_DIRECTIONS = set(["clinic", "healer", "hospital", "doctor"])
CITY_ALCHEMIST_DIRECTIONS = set(["alchemist", "potion shop", "lab", "laboratory", "pharmacy"])
CITY_MAGE_TOWER_DIRECTIONS = set(["mage tower", "wizard tower", "tower"])
CITY_TOWN_HALL_DIRECTIONS = set(["town hall", "hall", "capitol", "court"])
CITY_MARKETPLACE_DIRECTIONS = set(["marketplace", "market place", "market", "bazaar", "shops"])

CITY_MOUNTAIN_DIRECTIONS = set(["mountain", "north", "mountains", "base", "mountain base",
                           "base of the mountain", "base of the mountains", "mount"])
CITY_GRAVEYARD_DIRECTIONS = set(["graveyard", "west"])
CITY_FOREST_DIRECTIONS = set(["forest", "east"])
CITY_BEACH_DIRECTIONS = set(["beach", "south"])

MOUNTAIN_CITY_DIRECTIONS = set(["mara", "city", "south"])
MOUNTAIN_MINES_DIRECTIONS = set(["mines", "in", "inside", "down", "quarry", "b1", "entrance"])
MOUNTAIN_DOWN_DIRECTIONS = set(["down", "lower", "deeper"])
MOUNTAIN_UP_DIRECTIONS = set(["up"])
MOUNTAIN_OUT_DIRECTIONS = set(["out", "outside", "base", "mountain", "mountain base",
                              "base of the mountain"])
MOUNTAIN_HALL_MID_DIRECTIONS = set(["hall", "middle", "center", "entrance"])
MOUNTAIN_HALL_WEST_DIRECTIONS = set(["west", "left"])
MOUNTAIN_HALL_EAST_DIRECTIONS = set(["east", "right"])

BEACH_CITY_DIRECTIONS = set(["city", "mara", "north"])

FOREST_CITY_DIRECTIONS = set(["city", "mara", "west"])

GRAVEYARD_CITY_DIRECTIONS = set(["city", "mara", "east"])


#--------------------------------------------------------------------------------------------------
# Called when extension is loaded
#--------------------------------------------------------------------------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(GoCommand(bot))


#==================================================================================================
# GO COMMAND
#==================================================================================================
class GoCommand(commands.Cog, name="Go Command"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #----------------------------------------------------------------------------------------------
    # COMMAND: /go + direction
    #----------------------------------------------------------------------------------------------
    @discord.app_commands.command(name='go', description=DESCRIPTION)
    @discord.app_commands.describe(direction=DIRECTION_DESCRIPTION)
    async def go(self, interaction: discord.Interaction, direction: str):
        print(f"Received /go {direction} command from {interaction.user.display_name}")

        current_location = skale.get_player_location(interaction.user.id)
        previous_location = skale.get_previous_location(interaction.user.id)

        if not current_location:
            message = "No player data found... Try logging in again."
            await interaction.response.send_message(message, ephemeral=True)
            return

        message = f"`/go {direction}`\n"

        # get new location
        if direction == "back":
            new_location = previous_location
        else:
            new_location = self.get_new_location(current_location, direction.lower())

        if not new_location:
            # edge cases
            if direction == "shop":
                message += "Specify Blacksmith, Alchemist, or Marketplace"
                await interaction.response.send_message(message, ephemeral=True)
            # invalid direction
            else:
                message += "Can't Do That."
                await interaction.response.send_message(message, ephemeral=True)

        # same location
        elif new_location == current_location:
            message += f"You Are Already {Locations.location_names[new_location]}."
            await interaction.response.send_message(message, ephemeral=True)

        # go to new location
        else:
            current_region = Locations.get_region(current_location)
            new_region = Locations.get_region(new_location)

            message += "You "

            await self.set_channel_permissions(interaction, previous_location, current_location, new_location)
            skale.set_player_location(interaction.user.id, new_location)

            if current_region != new_region:
                await self.set_new_roles(interaction, current_region, new_region)
                message += "Travel Far And "

            new_channel = interaction.guild.get_channel(Locations.location_channel_ids[new_location])
            message += f"Find Yourself {Locations.location_names[new_location]}:\n{new_channel.mention}"
            await interaction.response.send_message(embed=discord.Embed(description=message), ephemeral=True)

    #----------------------------------------------------------------------------------------------
    # SET NEW ROLES
    #----------------------------------------------------------------------------------------------
    async def set_new_roles(self, interaction: discord.Interaction, current_region: int, new_region: int):
        # remove old region role
        role = interaction.guild.get_role(Locations.region_role_ids[current_region])
        await interaction.user.remove_roles(role)
        # add new region role
        role = interaction.guild.get_role(Locations.region_role_ids[new_region])
        await interaction.user.add_roles(role)

    #----------------------------------------------------------------------------------------------
    # SET CHANNEL PERMISSIONS
    #----------------------------------------------------------------------------------------------
    async def set_channel_permissions(
        self,
        interaction: discord.Interaction,
        prev_location: int,
        curr_location: int,
        new_location: int
    ):
        current_region = Locations.get_region(curr_location)
        new_region = Locations.get_region(new_location)

        # set access to regional chat channels
        if current_region != new_region:
            # disable old region
            region_channel = interaction.guild.get_channel(Locations.location_channel_ids[current_region])
            await region_channel.set_permissions(interaction.user, read_messages=False, send_messages=False)
            # enable new region
            region_channel = interaction.guild.get_channel(Locations.location_channel_ids[new_region])
            await region_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)

        # remove access to previous room channel
        if prev_location != new_location:
            prev_channel = interaction.guild.get_channel(Locations.location_channel_ids[prev_location])
            await prev_channel.set_permissions(interaction.user, read_messages=False, send_messages=False)
        
        # make current room channel readonly
        current_channel = interaction.guild.get_channel(Locations.location_channel_ids[curr_location])
        await current_channel.set_permissions(interaction.user, read_messages=True, send_messages=False)

        # make new room channel read and write
        new_channel = interaction.guild.get_channel(Locations.location_channel_ids[new_location])
        await new_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)

    #----------------------------------------------------------------------------------------------
    # GET NEW LOCATION
    #----------------------------------------------------------------------------------------------
    def get_new_location(self, current_location: int, direction: str) -> Optional[int]:
        # anywhere in city
        if Locations.get_region(current_location) == Locations.Region.CITY:
            if direction in CITY_OUTSIDE_DIRECTIONS:
                return Locations.CITY_OUTSIDE
            elif direction in CITY_SQUARE_DIRECTIONS:
                return Locations.CITY_SQUARE
            elif direction in CITY_ALCHEMIST_DIRECTIONS:
                return Locations.CITY_ALCHEMIST
            elif direction in CITY_BLACKSMITH_DIRECTIONS:
                return Locations.CITY_BLACKSMITH
            elif direction in CITY_CLINIC_DIRECTIONS:
                return Locations.CITY_CLINIC
            elif direction in CITY_MAGE_TOWER_DIRECTIONS:
                return Locations.CITY_MAGE_TOWER
            elif direction in CITY_MARKETPLACE_DIRECTIONS:
                return Locations.CITY_MARKETPLACE
            elif direction in CITY_MOUNTAIN_DIRECTIONS:
                return Locations.MOUNTAIN_BASE
            elif direction in CITY_FOREST_DIRECTIONS:
                return Locations.FOREST
            elif direction in CITY_BEACH_DIRECTIONS:
                return Locations.BEACH
            elif direction in CITY_GRAVEYARD_DIRECTIONS:
                return Locations.GRAVEYARD

        # anywhere in mountain
        elif Locations.get_region(current_location) == Locations.Region.MOUNTAIN:
            if direction in MOUNTAIN_OUT_DIRECTIONS:
                return Locations.MOUNTAIN_BASE

            # mountain base
            elif current_location == Locations.MOUNTAIN_BASE:
                if direction in MOUNTAIN_CITY_DIRECTIONS:
                    return Locations.CITY_OUTSIDE
                elif direction in MOUNTAIN_MINES_DIRECTIONS:
                    return Locations.MOUNTAIN_B1
            
            # B1
            elif current_location == Locations.MOUNTAIN_B1:
                if direction in MOUNTAIN_DOWN_DIRECTIONS:
                    return Locations.MOUNTAIN_B2
                elif direction in MOUNTAIN_UP_DIRECTIONS:
                    return Locations.MOUNTAIN_BASE

            # B2
            elif current_location == Locations.MOUNTAIN_B2:
                if direction in MOUNTAIN_DOWN_DIRECTIONS:
                    return Locations.MOUNTAIN_HALL_MID
                elif direction in MOUNTAIN_UP_DIRECTIONS:
                    return Locations.MOUNTAIN_B1
            
            # HALL MID
            elif current_location == Locations.MOUNTAIN_HALL_MID:
                if direction in MOUNTAIN_DOWN_DIRECTIONS:
                    return Locations.MOUNTAIN_B4
                elif direction in MOUNTAIN_UP_DIRECTIONS:
                    return Locations.MOUNTAIN_B2
                elif direction in MOUNTAIN_HALL_EAST_DIRECTIONS:
                    return Locations.MOUNTAIN_HALL_EAST
                elif direction in MOUNTAIN_HALL_WEST_DIRECTIONS:
                    return Locations.MOUNTAIN_HALL_WEST

            # HALL EAST
            elif current_location == Locations.MOUNTAIN_HALL_EAST:
                if direction in MOUNTAIN_DOWN_DIRECTIONS:
                    return Locations.MOUNTAIN_B4
                elif direction in MOUNTAIN_UP_DIRECTIONS:
                    return Locations.MOUNTAIN_B2
                elif direction in MOUNTAIN_HALL_MID_DIRECTIONS or \
                    direction in MOUNTAIN_HALL_WEST_DIRECTIONS:
                    return Locations.MOUNTAIN_HALL_MID

            # HALL WEST
            elif current_location == Locations.MOUNTAIN_HALL_WEST:
                if direction in MOUNTAIN_DOWN_DIRECTIONS:
                    return Locations.MOUNTAIN_B4
                elif direction in MOUNTAIN_UP_DIRECTIONS:
                    return Locations.MOUNTAIN_B2
                elif direction in MOUNTAIN_HALL_MID_DIRECTIONS or \
                    direction in MOUNTAIN_HALL_EAST_DIRECTIONS:
                    return Locations.MOUNTAIN_HALL_MID

            # B4
            elif current_location == Locations.MOUNTAIN_B4:
                if direction in MOUNTAIN_UP_DIRECTIONS:
                    return Locations.MOUNTAIN_HALL_MID

        # beach
        elif Locations.get_region(current_location) == Locations.Region.BEACH:
            if direction in BEACH_CITY_DIRECTIONS:
                return Locations.CITY_OUTSIDE

        # forest
        elif Locations.get_region(current_location) == Locations.Region.FOREST:
            if direction in FOREST_CITY_DIRECTIONS:
                return Locations.CITY_OUTSIDE

        # graveyard
        elif Locations.get_region(current_location) == Locations.Region.GRAVEYARD:
            if direction in GRAVEYARD_CITY_DIRECTIONS:
                return Locations.CITY_OUTSIDE
        