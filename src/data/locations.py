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
        CITY_OUTSIDE: "Outside the North Gate of the City of Mara",
        CITY_ALCHEMIST: "At the Alchemist's Lab",
        CITY_BLACKSMITH: "At the Blacksmith's Shop",
        CITY_CLINIC: "At the Clinic",
        CITY_MAGE_TOWER: "At the Mage Tower",
        CITY_MARKETPLACE: "At the Marketplace",
        CITY_SQUARE: "In Mara, at the Town Square",
        CITY_TOWN_HALL: "At the Town Hall",
        MOUNTAIN_BASE: "At the Base of the Mountain",
        MOUNTAIN_B1: "In B1 of the Mines",
        MOUNTAIN_B2: "In B2 of the Mines",
        MOUNTAIN_HALL_MID: "In the Grand Hall",
        MOUNTAIN_HALL_WEST: "In the West Wing of the Grand Hall",
        MOUNTAIN_HALL_EAST: "In the East Wing of the Grand Hall",
        MOUNTAIN_B4: "In B4 of the Mines",
        BEACH: "At the Beach",
        FOREST: "In the Forest",
        GRAVEYARD: "At the Graveyard"
    }

    def get_region(location: int) -> int:
        return int(location/100)
