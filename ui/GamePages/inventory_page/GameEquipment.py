from xml.etree.ElementTree import ElementTree, Element
from ui.GamePages.inventory_page.SlotsGroup import SlotsGroup
from game_objects.items import ItemTransactions
from game_objects.items import ItemTypes


class GameEquipment(SlotsGroup):
    def __init__(self, gameRoot, page):
        super(GameEquipment, self).__init__(gameRoot, page)
        self.default_icons = {}

    def setUpSlots(self, element):
        for slot in self.gameRoot.lengine.the_hero.equipment.all_slots:
            name_slot = slot.name.lower()
            if name_slot == 'ring_1':
                name_slot = 'ring1'
            elif name_slot == 'ring_2':
                name_slot = 'ring2'
            item: Element = self.page.find_element(
                element, name=f'equip_slot_{name_slot}')
            self.default_icons[f'equip_slot_{name_slot}'] = item.get(
                'icon', 'default.png')
            self.slots[f'equip_slot_{name_slot}'] = slot
            if slot.content is not None:
                item.set('icon', slot.content.icon)

    def update_attr(self):
        for key, slot in self.slots.items():
            item = self.page.items.get(key)
            if item is not None:
                if slot.content is None:
                    item.setPixmapIcon(self.default_icons[key])
                else:
                    item.setPixmapIcon(slot.content.icon)
