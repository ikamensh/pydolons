from __future__ import annotations
from game_objects.items import ItemTypes
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from DreamGame import DreamGame
    from game_objects.battlefield_objects import Unit
    from game_objects.items import Slot, ItemTypes

class Item:
    def __init__(self, name: str, item_type: ItemTypes, *, game: DreamGame=None, icon=None):
        assert isinstance(name, str)
        assert isinstance(item_type, ItemTypes)
        self.item_type = item_type
        self.name = name
        self.game = game
        self.owner: Unit = None
        self.slot = None
        self.icon = icon or "generic_item.png"

    @property
    def tooltip_info(self):
        return {"name": f"{self.name}",
                "type": f"{self.item_type}"}

    def __repr__(self):
        return f"Item: {self.name}"