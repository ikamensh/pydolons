from __future__ import annotations
from game_objects.items import Item
from typing import TYPE_CHECKING
from mechanics.events import ItemDroppedEvent
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit
    from game_objects.items import ItemTypes


class Slot:
    def __init__(self, name:str, item_type : ItemTypes = None, owner: Unit = None):
        self.name = name
        self.item_type = item_type
        self.owner = owner
        self._content = None

    @property
    def content(self) -> Item:
        return self._content

    @content.setter
    def content(self, item):

        if self.content:
            raise Exception("Remove existing item first.")

        if not self.check_type_match(item):
            raise Exception("Invalid item type")

        self._content = item
        item.slot = self
        item.owner = self.owner

        if self.owner:
            try:
                item.game = self.owner.game
                if hasattr(item, "on_equip"):
                    item.on_equip(self)
            except AttributeError:
                pass

    def drop(self):
        if self.content:
            item = self.pop_item()
            ItemDroppedEvent(item)

    def check_type_match(self, item):
        if self.item_type is None:
            return True
        elif item is None:
            return True
        else:
            return self.item_type is item.item_type


    def swap_item(self, other_slot: Slot):
        if self.check_type_match(other_slot.content) and other_slot.check_type_match(self.content):
            self._content, other_slot._content = other_slot.pop_item(), self.pop_item()
            return True
        else:
            return False

    def pop_item(self):
        if self.content is None:
            return

        item = self.content
        self._content = None
        if self.owner:
            if hasattr(item, "on_unequip"):
                item.on_unequip(self)
            self.owner.recalc()
        item.owner = None
        return item

    @property
    def tooltip_info(self):
        if self.content:
            return self.content.tooltip_info
        else:
            return {"Slot": f"{self.name}",
                    "Type": f"{self.item_type}"}

    def __repr__(self):
        return f"{self.owner}'s {self.name} slot with {self.content}"


