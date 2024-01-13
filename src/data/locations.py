from typing import Any, Dict, List
from data.items import Items

class Locations:
    class Region:
        CITY = 1
        MOUNTAIN = 2
        BEACH = 3
        FOREST = 4
        GRAVEYARD = 5

    CITY_OUTSIDE = 100
    CITY_ALCHEMIST = 101
    CITY_BLACKSMITH = 102
    CITY_CLINIC = 103
    CITY_MAGE_TOWER = 104
    CITY_MARKETPLACE = 105
    CITY_SQUARE = 106
    CITY_TOWN_HALL = 107

    MOUNTAIN_BASE = 200
    MOUNTAIN_B1 = 201
    MOUNTAIN_B2 = 202
    MOUNTAIN_HALL_MID = 203
    MOUNTAIN_HALL_WEST = 204
    MOUNTAIN_HALL_EAST = 205
    MOUNTAIN_B4 = 206

    BEACH = 300
    FOREST = 400
    GRAVEYARD = 500

    region_role_ids = {
        Region.CITY: 1194716787686772846,
        Region.MOUNTAIN: 1194475616578322442,
        Region.BEACH: 1194476107513217084,
        Region.FOREST: 1194476158268485825,
        Region.GRAVEYARD: 1194476243421233173
    }

    location_channel_ids = {
        Region.CITY: 1194464771144171530,
        CITY_OUTSIDE: 1194464847803465839,
        CITY_ALCHEMIST: 1194465045703303228,
        CITY_BLACKSMITH: 1194465003948998796,
        CITY_CLINIC: 1194465195452547193,
        CITY_MAGE_TOWER: 1194465086295785553,
        CITY_MARKETPLACE: 1194465157850615828,
        CITY_SQUARE: 1194803351536287846,
        CITY_TOWN_HALL: 1194465119552426055,
        Region.MOUNTAIN: 1194465777097646191,
        MOUNTAIN_BASE: 1194465547816013974,
        MOUNTAIN_B1: 1194465647497850880,
        MOUNTAIN_B2: 1194465917611032698,
        MOUNTAIN_HALL_MID: 1194465979300843612,
        MOUNTAIN_HALL_WEST: 1194466048360067102,
        MOUNTAIN_HALL_EAST: 1194466118853742622,
        MOUNTAIN_B4: 1194466152722739281,
        Region.BEACH: 1194466274470797362,
        BEACH: 1194466274470797362,
        Region.FOREST: 1194466311124828250,
        FOREST: 1194466311124828250,
        Region.GRAVEYARD: 1194466338350055434,
        GRAVEYARD: 1194466338350055434
    }

    location_names = {
        CITY_OUTSIDE: "outside the North Gate of the City of Mara",
        CITY_ALCHEMIST: "at the Alchemist's Lab",
        CITY_BLACKSMITH: "at the Blacksmith's Shop",
        CITY_CLINIC: "at the Clinic",
        CITY_MAGE_TOWER: "at the Mage Tower",
        CITY_MARKETPLACE: "at the Marketplace",
        CITY_SQUARE: "in Mara, at the Town Square",
        CITY_TOWN_HALL: "at the Town Hall",
        MOUNTAIN_BASE: "at the base of the Mountain",
        MOUNTAIN_B1: "in B1 of the Mines",
        MOUNTAIN_B2: "in B2 of the Mines",
        MOUNTAIN_HALL_MID: "in the Grand Hall",
        MOUNTAIN_HALL_WEST: "in the West Wing of the Grand Hall",
        MOUNTAIN_HALL_EAST: "in the East Wing of the Grand Hall",
        MOUNTAIN_B4: "in B4 of the Mines",
        BEACH: "at the Beach",
        FOREST: "in the Forest",
        GRAVEYARD: "at the Graveyard"
    }

    location_descriptions = {
        CITY_OUTSIDE: "You can't see anything , <@267801271887593478> didn't write it yet.",
        CITY_ALCHEMIST: "You can't see anything , <@267801271887593478> didn't write it yet.",
        CITY_BLACKSMITH: (
            "You see Kate the blacksmith hammering away at the anvil.\n"
            "You see things for sale.\n"
            "The exit back to __Mara__ is behind you."
        ),
        CITY_CLINIC: "You can't see anything , <@267801271887593478> didn't write it yet.",
        CITY_MAGE_TOWER: "You can't see anything , <@267801271887593478> didn't write it yet.",
        CITY_MARKETPLACE: "You can't see anything , <@267801271887593478> didn't write it yet.",
        CITY_SQUARE: (
            "Nearby, you see a __Blacksmith__.\n"
            "In the distance, you see the north gate that leads to the __Mountain__."),
        CITY_TOWN_HALL: "You can't see anything , <@267801271887593478> didn't write it yet.",
        MOUNTAIN_BASE: (
            "You find yourself at the base of the Mountains.\n"
            "You see the entrance to the __Mines__. Behind you is the city of __Mara__."
        ),
        MOUNTAIN_B1: (
            "You just see regular rocks.\n"
            "You might need to go deeper to find ores."
        ),
        MOUNTAIN_B2: (
            "You see the stairs __up__ and the stairs __down__.\n"
            "You see rocks with glints of Copper, ready to __mine__."
        ),
        MOUNTAIN_HALL_MID: "You can't see anything , <@267801271887593478> didn't write it yet.",
        MOUNTAIN_HALL_EAST: "You can't see anything , <@267801271887593478> didn't write it yet.",
        MOUNTAIN_HALL_WEST: "You can't see anything , <@267801271887593478> didn't write it yet.",
        MOUNTAIN_B4: (
            "You see the stairs __up__ and the stairs __down__.\n",
            "You see <Skeleton> blocking the stairs that go __down__.\n",
            "You look carefully at <Skeleton>. It is LVL 1. You can __attack__ it.\n",
            "You see rocks with glints of Copper, ready to __mine__."
        ),
        GRAVEYARD: "You can't see anything , <@267801271887593478> didn't write it yet.",
        FOREST: "You can't see anything , <@267801271887593478> didn't write it yet.",
        BEACH: "You can't see anything, <@267801271887593478> didn't write it yet."
    }

    shop_items: Dict[int, List[Dict[str, Any]]] = {
        CITY_ALCHEMIST: [],
        CITY_BLACKSMITH: [
            {"id": Items.COPPER_SWORD_UNEQUIPPED, "price": 1000},
            {"id": Items.COPPER_ORE, "price": 900},
            {"id": Items.HUNDRED_GOLD, "price": -100}
        ],
        CITY_CLINIC: [],
        CITY_MAGE_TOWER: [],
        CITY_MARKETPLACE: []
    }

    def get_region(location: int) -> int:
        return int(location/100)
