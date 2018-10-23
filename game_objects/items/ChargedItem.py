from game_objects.items import Item, ItemTypes
from game_objects.attributes import DynamicParameter
from mechanics.events import ItemUsedUpEvent
from mechanics.actives import Active, ActiveTags, Cost

#Design: ensure item has game variable as soon as it enters any interactable containers.
class ChargedItem(Item):

    charges = DynamicParameter("max_charges", on_zero_callbacks=[ItemUsedUpEvent])

    def __init__(self, name, max_charges=1, *, targeting_cls=None, conditions=None, atb_cost=0.5,
                 use_callbacks, tags=None, game=None, icon=None):
        super().__init__(name, ItemTypes.CHARGED, game=game, icon=icon)
        assert isinstance(name, str)
        assert isinstance(max_charges, int)
        self.max_charges = max_charges

        def decrease_charges_cb(active, target):
            self.charges -= 1

        self.active = Active(targeting_cls, conditions, Cost(readiness=atb_cost), name=f"Use {self}",
                             callbacks=use_callbacks +[decrease_charges_cb], tags=[ActiveTags.CHARGED_ITEM] + (tags or []))

    def on_equip(self, slot):
        if slot.item_type == self.item_type:
            self.owner.give_active(self.active)

    def on_unequip(self, slot):
        if slot.item_type == self.item_type:
            self.owner.remove_active(self.active)








