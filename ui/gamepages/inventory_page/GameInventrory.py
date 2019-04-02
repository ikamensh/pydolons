from xml.etree.ElementTree import Element
from game_objects.items.on_unit.Slot import Slot
from game_objects.items import ItemTransactions
from ui.gamepages.inventory_page.SlotsGroup import SlotsGroup


class GameInventrory(SlotsGroup):
    def __init__(self, gameRoot, page):
        super(GameInventrory, self).__init__(gameRoot, page)

    def setUpSlots(self, elemnt):
        for slot in self.gameRoot.lengine.the_hero.inventory:
            self.slots['inventory_slot_' + str(self._l)] = slot
            elemnt.append(self.create_slot(slot))

    def create_slot(self, slot:Slot, width=128, space=10):
        self._width += width
        self._space += space
        attr = {}
        attr['name'] = 'inventory_slot_' + str(self._l)
        attr['position'] = "inherit"
        attr['top'] = '10'
        attr['left'] = str(width * self._l + space * self._l)
        attr['height'] = '128'
        attr['width'] = '128'
        attr['input'] = 'button'
        if slot.content is None:
            attr['icon'] = 'cha_page_elemnt_bg.png'
        else:
            attr['icon'] = slot.content.icon
        tag = 'item'
        self._l += 1
        return Element(tag, attr)








