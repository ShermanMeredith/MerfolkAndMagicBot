import json
import pickle
from collections import defaultdict
from dataclasses import dataclass
from os import environ
from typing import Any, DefaultDict, Dict, List, Optional

from web3 import Web3
from web3.contract.contract import Contract

import data.abis as abis
from data.locations import Locations


@dataclass
class Inventory:
    gold_balance: int
    items: DefaultDict[int, int]

STARTING_STATS = {"current_hp": 20, "max_hp": 20, "base_attack": 1, "base_defense": 1, "base_speed": 13}


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
    #def get_character_info(self, user_id: int) -> CharacterInfo:
        #character_id = self.get_character_id(user_id)
        #result = self.character_contract.functions.get_character_info(character_id)
        #return CharacterInfo(result[0], result[1], result[2], Location(result[3], result[4]))


# TODO: replace with actual skale data
PLAYER_LOCATIONS_FILEPATH = "src/data/player_locations.json"
PLAYER_STATS_FILEPATH = "src/data/player_stats.json"
PLAYER_INVENTORIES_FILEPATH = "src/data/player_inventories.pkl"

#----------------------------------------------------------------------------------------------
# GET PLAYER LOCATION
#----------------------------------------------------------------------------------------------
def get_player_location(member_id: int) -> Optional[int]:
    player_locations: Dict[str, str] = {}
    with open(PLAYER_LOCATIONS_FILEPATH) as f:
        try:
            player_locations = json.load(f)
        except:
            return None

    if str(member_id) not in player_locations:
        return None

    current_location = player_locations[str(member_id)]["current_location"]
    if current_location:
        return int(current_location)
    else:
        return None

#----------------------------------------------------------------------------------------------
# GET PREVIOUS LOCATION
#----------------------------------------------------------------------------------------------
def get_previous_location(member_id: int) -> Optional[int]:
    player_locations: Dict[str, str] = {}
    with open(PLAYER_LOCATIONS_FILEPATH) as f:
        try:
            player_locations = json.load(f)
        except:
            return None

    if str(member_id) not in player_locations:
        return None

    previous_location = player_locations[str(member_id)]["previous_location"]
    if previous_location:
        return int(previous_location)
    else:
        return None

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

    if str(member_id) not in player_locations or not player_locations[str(member_id)]:
        player_locations[str(member_id)] = {
            "current_location": None,
            "previous_location": None
        }
    player_locations[str(member_id)]["previous_location"] = player_locations[str(member_id)]["current_location"]
    player_locations[str(member_id)]["current_location"] = location_id

    with open(PLAYER_LOCATIONS_FILEPATH, 'w') as f:
        json.dump(player_locations, f)

#----------------------------------------------------------------------------------------------
# GET PLAYER INVENTORY
#----------------------------------------------------------------------------------------------
def get_player_inventory(member_id: int) -> Inventory:
    player_inventory = Inventory(0, defaultdict(int))

    with open(PLAYER_INVENTORIES_FILEPATH, "rb") as f:
        try:
            player_inventories = pickle.load(f)
            if str(member_id) in player_inventories and player_inventories[str(member_id)]:
                player_inventory = player_inventories[str(member_id)]
            else:
                set_player_inventory(member_id, player_inventory)
        except:
            set_player_inventory(member_id, player_inventory)

    return player_inventory

#----------------------------------------------------------------------------------------------
# SET PLAYER INVENTORY
#----------------------------------------------------------------------------------------------
def set_player_inventory(member_id: int, inventory: Inventory):
    player_inventories: Dict[str, Inventory] = {}
    with open(PLAYER_INVENTORIES_FILEPATH, "rb") as f:
        try:
            player_inventories = pickle.load(f)
        except:
            pass

    player_inventories[str(member_id)] = inventory

    with open(PLAYER_INVENTORIES_FILEPATH, 'wb') as f:
        f.write(pickle.dumps(player_inventories))

#--------------------------------------------------------------------------------------------------
# GET SHOP ITEMS
#--------------------------------------------------------------------------------------------------
def get_shop_items(location_id: int) -> Optional[List[Dict[str, Any]]]:
    return Locations.shop_items.get(location_id, None)

#--------------------------------------------------------------------------------------------------
# GET PLAYER STATS
#--------------------------------------------------------------------------------------------------
def get_player_stats(member_id: int) -> Dict[str, int]:
    player_stats: Dict[str, int] = {}
    with open(PLAYER_STATS_FILEPATH) as f:
        try:
            all_player_stats = json.load(f)
            if str(member_id) in all_player_stats:
                player_stats = all_player_stats[str(member_id)]
            else:
                player_stats = STARTING_STATS
                set_player_stats(member_id, player_stats)

        except:
            player_stats = STARTING_STATS

    return player_stats


#--------------------------------------------------------------------------------------------------
# SET PLAYER STATS
#--------------------------------------------------------------------------------------------------
def set_player_stats(member_id: int, player_stats: Dict[str, int]):
    all_player_stats: Dict[str, Dict[str, int]] = {}
    with open(PLAYER_STATS_FILEPATH) as f:
        try:
            all_player_stats = json.load(f)
        except:
            pass

    all_player_stats[str(member_id)] = player_stats

    with open(PLAYER_STATS_FILEPATH, 'w') as f:
        json.dump(all_player_stats, f)
