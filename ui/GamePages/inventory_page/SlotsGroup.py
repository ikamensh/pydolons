from xml.etree.ElementTree import ElementTree, Element
from game_objects.items.on_unit.Slot import Slot
from game_objects.items import ItemTransactions


class SlotsGroup:
    def __init__(self, gameRoot, page=None):
        self.gameRoot = gameRoot
        self.page = page
        self._l = 0
        self._width = 0
        self._height = 0
        self._space = 0
        self.slots = {}
        self.emty_icon = 'cha_page_elemnt_bg.png'

    @property
    def width(self):
        return self._width + self._space

    @property
    def len(self):
        return self._l

    def setUpSlots(self, element: Element):
        pass

    def create_slot(self, slot: Slot, width=128, height=128, space=10):
        pass

    def update_attr(self):
        for key, slot in self.slots.items():
            item = self.page.items.get(key)
            if item is not None:
                if slot.content is None:
                    item.setPixmapIcon(self.emty_icon)
                else:
                    item.setPixmapIcon(slot.content.icon)

    def getMovedSlot(self, item):
        moved_slot = self.slots.get(item.name)
        if moved_slot is not None:
            if moved_slot.content is not None:
                self.page.moved_slot.setPixmapIcon(moved_slot.content.icon)
            else:
                return None
        return moved_slot

    def setDict(self, data):
        result = ''
        for k, v in data.items():
            result = result + k + ' : ' + v + '\n'
        return result
