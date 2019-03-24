from ui.GamePages.inventory_page.SlotsGroup import SlotsGroup
from game_objects.items import ItemTransactions

from xml.etree.ElementTree import ElementTree, Element


class GameShop(SlotsGroup):
    def __init__(self, gameRoot, page):
        super(GameShop, self).__init__(gameRoot, page)

    def setUpSlots(self, element):
        for slot in self.gameRoot.game.shop.inventory:
            self.slots['shop_slot_' + str(self._l)] = slot
            element.append(self.create_slot(slot))

    def create_slot(self, slot, width=128, height=128, space=10):
        self._width += width
        self._space += space
        attr = {}
        attr['name'] = 'shop_slot_' + str(self._l)
        attr['position'] = "inherit"
        attr['top'] = '10'
        attr['left'] = str(width * self._l + space * self._l)
        attr['height'] = '128'
        attr['width'] = '128'
        attr['input'] = 'button'
        if slot.content is None:
            attr['icon'] = self.emty_icon
        else:
            attr['icon'] = slot.content.icon
        tag = 'item'
        self._l += 1
        return Element(tag, attr)

    def show_info(self, slot):
        if slot.content is None:
            return slot.tooltip_info
        else:
            info = slot.tooltip_info
            info['price'] = str(slot.content.price)
            return info
