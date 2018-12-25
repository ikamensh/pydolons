from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.items import ChargedItem

class ItemUsedUpEvent(Event):
    channel = EventsChannels.UsedUpChannel

    def __init__(self, item: ChargedItem):
        self.item = item
        super().__init__(item.game)

    def check_conditions(self):
        return True

    def resolve(self):
        self.item.slot.pop_item()

    def __repr__(self):
        if self.item.owner:
            return f"{self.item.owner}'s {self.item} was used up."
        else:
            return f"{self.item} was used up."