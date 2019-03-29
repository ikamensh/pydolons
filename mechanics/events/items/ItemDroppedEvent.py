from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.items import Item


class ItemDroppedEvent(Event):
    channel = EventsChannels.DropChannel

    def __init__(self, item: Item, cell=None):
        self.item = item
        g = item.game
        if cell:
            location = cell
        else:
            if item.owner:
                location = g.bf.unit_locations[item.owner]
            else:
                location = g.random.sample(g.bf.all_cells, 1)[0]
        self.location = location

        super().__init__(g, logging=True)

    def check_conditions(self):
        return True

    def resolve(self):
        if self.item.slot:
            self.item.slot.pop_item()
        pass
        # TODO enable pickup of dropped items

    def __repr__(self):
        return f"{self.item} was dropped at {self.location}."
