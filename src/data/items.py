class ItemType:
    NONE = 0
    INGREDIENT = 1
    EQUIPPABLE = 2
    EQUIPPED = 3
    CONSUMABLES = 4

class Items:
    HUNDRED_GOLD = 1

    COPPER_ORE = 101
    IRON_ORE = 102
    COAL = 103
    MITHRIL = 104

    COPPER_SWORD_UNEQUIPPED = 201
    IRON_SWORD_UNEQUIPPED = 202
    STEEL_SWORD_UNEQUIPPED = 203
    MITHRIL_SWORD_UNEQUIPPED = 204

    COPPER_SWORD_EQUIPPED = 301
    IRON_SWORD_EQUIPPED = 302
    STEEL_SWORD_EQUIPPED = 303
    MITHRIL_SWORD_EQUIPPED = 304

    MINOR_POTION = 401
    LIGHT_POTION = 402
    STANDARD_POTION = 403
    GREATER_POTION = 404
    SUPER_POTION = 405

    item_names = {
        HUNDRED_GOLD: "100 Gold",
        
        COPPER_ORE: "Copper Ore",
        IRON_ORE: "Iron Ore",
        COAL: "Coal",
        MITHRIL: "Mithril",
        
        COPPER_SWORD_UNEQUIPPED: "Copper Sword",
        IRON_SWORD_UNEQUIPPED: "Iron Sword",
        STEEL_SWORD_UNEQUIPPED: "Steel Sword",
        MITHRIL_SWORD_UNEQUIPPED: "Mithril Sword",

        COPPER_SWORD_EQUIPPED: "Copper Sword",
        IRON_SWORD_EQUIPPED: "Iron Sword",
        STEEL_SWORD_EQUIPPED: "Steel Sword",
        MITHRIL_SWORD_EQUIPPED: "Mithril Sword",

        MINOR_POTION: "Minor Healing Potion",
        LIGHT_POTION: "Light Healing Potion",
        STANDARD_POTION: "Healing Potion",
        GREATER_POTION: "Greater Healing Potion",
        SUPER_POTION: "Super Healing Potion"
    }

    def get_item_type(item_id: int) -> int:
        return int(item_id/100)
    
    def get_equipped_version(item_id: int) -> int:
        return 300 + (item_id % 100)

    def get_unequipped_version(item_id: int) -> int:
        return 200 + (item_id % 100)
