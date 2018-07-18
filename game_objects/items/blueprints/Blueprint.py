from game_objects.items import Item, ItemTypes
from game_objects.items.materials.MaterialTypes import durability_per_material

class Blueprint(Item):
    durability_per_rarity = 35

    def __init__(self, name, target_item_type, rarity, durability, material_count, material_type):
        super().__init__(name, ItemTypes.BLUEPRINT)
        self.target_item_type = target_item_type
        self.name = name
        self.rarity = rarity
        self.durability = durability or rarity * Blueprint.durability_per_rarity
        self.material_count = material_count
        self.material_type = material_type


    def item_durability(self, rarity):
        return self.durability * rarity * durability_per_material[self.material_type]

