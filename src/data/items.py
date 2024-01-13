class ItemType:
    NONE = 0
    INGREDIENT = 1
    EQUIPPABLE = 2
    EQUIPPED = 3

class Items:
    HUNDRED_GOLD = 1
    COPPER_ORE = 101
    COPPER_SWORD_UNEQUIPPED = 201
    COPPER_SWORD_EQUIPPED = 301

    item_names = {
        HUNDRED_GOLD: "100 Gold",
        COPPER_ORE: "Copper Ore",
        COPPER_SWORD_UNEQUIPPED: "Copper Sword",
        COPPER_SWORD_EQUIPPED: "Copper Sword"
    }

    def get_item_type(item_id: int) -> int:
        return int(item_id/100)
