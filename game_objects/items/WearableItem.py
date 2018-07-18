from game_objects.items import Item
from game_objects.battlefield_objects.attributes import DynamicParameter
from mechanics.events import ItemDestroyedEvent

class WearableItem(Item):

    durability = DynamicParameter("max_durability", on_zero_callbacks=[ItemDestroyedEvent])

    def __init__(self, name, item_type, *, blueprint=None, quality=None, material=None, max_durability=None):
        super().__init__(name, item_type)
        assert isinstance(name, str)
        self.blueprint = blueprint
        self.quality = quality
        self.material = material
        self.max_durability = max_durability

    @property
    def durability_factor(self):
        durability_factor = 0.5 + 0.5 * self.durability / self.max_durability
        return durability_factor