from game_objects.items import Item
from game_objects.attributes import DynamicParameter
from mechanics.events import ItemDestroyedEvent

#Design: ensure item has game variable as soon as it enters any interactable containers.
class WearableItem(Item):

    durability = DynamicParameter("max_durability", on_zero_callbacks=[ItemDestroyedEvent])
    energy = DynamicParameter("max_energy")

    def __init__(self, name, item_type, *, blueprint=None, quality=None, material=None,
                 max_durability=None, actives = None,
                 game=None):
        super().__init__(name, item_type, game=game)
        assert isinstance(name, str)
        self.blueprint = blueprint
        self.quality = quality
        self.material = material
        self.max_durability = max_durability
        self.rarity = self.calc_rarity()

        self.max_complexity = self.material.magic_complexity * self.rarity if self.material else 0
        self.max_energy = self.material.magic_complexity * self.rarity ** 2 if self.material else 50
        self.active_enchantment = None
        self.bonuses = []
        self.actives = actives or []

    @property
    def durability_factor(self):
        durability_factor = 0.5 + 0.5 * self.durability / self.max_durability
        return durability_factor

    def calc_rarity(self):
        mr = self.material.rarity if self.material else 1
        qr = self.quality.rarity if self.quality else 1
        br = self.blueprint.rarity if self.blueprint else 1

        total_rarity = mr * qr * br
        return total_rarity


    def on_equip(self, slot):
        if slot.item_type == self.item_type:
            for active in self.actives:
                self.owner.give_active(active)

    def on_unequip(self, slot):
        if slot.item_type == self.item_type:
            for active in self.actives:
                self.owner.remove_active(active)



