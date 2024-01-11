import json
from os import environ
from typing import Dict, Optional

from web3 import Web3
from web3.contract.contract import Contract

import data.abis as abis
from utils.types import CharacterInfo, Location
from utils.accounts import user_accounts


#==================================================================================================
#==================================================================================================
class Skale:

    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------
    def __init__(self):
        endpoint = environ.get("SKALE_ENDPOINT")
        self.skale_conn = Web3(Web3.HTTPProvider(endpoint, request_kwargs={'timeout':15}))
        self.character_contract: Contract = self.skale_conn.eth.contract("asdf", abi=abis.character_info)
        self.movement_contract: Contract = self.skale_conn.eth.contract("asdf", abi=abis.locations)

    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------
    def get_character_info(self, user_id: int) -> CharacterInfo:
        character_id = self.get_character_id(user_id)
        result = self.character_contract.functions.get_character_info(character_id)
        return CharacterInfo(result[0], result[1], result[2], Location(result[3], result[4]))

    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------
    def get_character_id(self, user_id: int) -> int:
        return 1

    def set_character_name(self, name: str):
        pass



# TODO: replace with actual database
PLAYER_LOCATIONS_FILEPATH = "src/data/player_locations.json"

#----------------------------------------------------------------------------------------------
# GET PLAYER LOCATION
#----------------------------------------------------------------------------------------------
def get_player_location(member_id: int) -> Optional[int]:
    if member_id not in user_accounts:
        return None

    player_locations: Dict[str, str] = {}
    with open(PLAYER_LOCATIONS_FILEPATH) as f:
        try:
            player_locations = json.load(f)
        except:
            return None

    if str(member_id) not in player_locations:
        return None

    return int(player_locations[str(member_id)]["current_location"])

#----------------------------------------------------------------------------------------------
# GET PREVIOUS LOCATION
#----------------------------------------------------------------------------------------------
def get_previous_location(member_id: int) -> Optional[int]:
    if member_id not in user_accounts:
        return None

    player_locations: Dict[str, str] = {}
    with open(PLAYER_LOCATIONS_FILEPATH) as f:
        try:
            player_locations = json.load(f)
        except:
            return None

    if str(member_id) not in player_locations:
        return None

    return int(player_locations[str(member_id)]["previous_location"])


#----------------------------------------------------------------------------------------------
# SET PLAYER LOCATION
#----------------------------------------------------------------------------------------------
def set_player_location(member_id: int, location_id: int):
    player_locations: Dict[str, str] = {}
    with open(PLAYER_LOCATIONS_FILEPATH) as f:
        try:
            player_locations = json.load(f)
        except:
            pass

    player_locations[str(member_id)]["previous_location"] = player_locations[str(member_id)]["current_location"]
    player_locations[str(member_id)]["current_location"] = location_id

    with open(PLAYER_LOCATIONS_FILEPATH, 'w') as f:
        json.dump(player_locations, f)
        f.close()
