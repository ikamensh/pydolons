from game_objects.items import Item, ItemTypes
from game_objects.items.materials.MaterialTypes import durability_per_material
from my_utils.utils import tractable_value


class Blueprint(Item):
    durability_per_rarity = 35
    BASE_PRICE = 5

    def __init__(
            self,
            name,
            target_item_type,
            rarity,
            durability,
            material_count,
            material_type):
        assert durability is None or 0.05 <= durability <= 20

        super().__init__(name, ItemTypes.BLUEPRINT)
        self.target_item_type = target_item_type
        self.name = name
        self.rarity = rarity
        self.durability = (durability or 1) * rarity * \
            Blueprint.durability_per_rarity
        self.material_count = material_count
        self.material_type = material_type

        self.value = self.rarity ** 2.2 * (1 + (durability or 1)) ** 2 / 3
        self.bonuses = []

    @property
    def price(self):
        return tractable_value(Blueprint.BASE_PRICE *
                               (self.value ** 4.1 + 2 * self.value ** 3.3 + 1))

    def item_durability(self, rarity):
        return self.durability * rarity * \
            durability_per_material[self.material_type]

    # @property
    # def price(self):
    #     return
