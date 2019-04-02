from ui.gamepages.inventory_page.SlotsGroup import SlotsGroup
from xml.etree.ElementTree import Element


class GameQuickItems(SlotsGroup):
    def __init__(self, gameRoot, page):
        super(GameQuickItems, self).__init__(gameRoot=gameRoot, page=page)

    def setUpSlots(self, element: Element):
        for slot in self.gameRoot.lengine.the_hero.quick_items:
            print(slot)
            self.slots['quickitems_slot_' + str(self._l)] = slot
            element.append(self.create_slot(slot))

