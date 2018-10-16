from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.items import WearableItem

class ItemDestroyedEvent(Event):
    channel = EventsChannels.ItemDestroyedChannel

    def __init__(self, item: WearableItem):
        self.item = item
        super().__init__(item.game)

    def check_conditions(self):
        return True

    def resolve(self):
        if self.item.slot:
            self.item.slot.pop_item()
        if self.item.owner and self.item.blueprint and self.item.material:
            self.item.owner.inventory.add(self.item.blueprint)
            self.item.owner.inventory.add(self.item.material.to_pieces(self.item.blueprint.material_count))

    def __repr__(self):
        if self.item.owner:
            return f"{self.item.owner}'s {self.item} was destroyed"
        else:
            return f"{self.item} was destroyed"