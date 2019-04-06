from ui.pages.inventory_page.SlotsGroup import SlotsGroup
from game_objects.items import ItemTransactions


class SlotMoveMaster:
    def __init__(self, gameRoot, page):
        self.gameRoot =gameRoot
        self.page = page
        self.moved_slot = None
        self.emty_icon = 'cha_page_elemnt_bg.png'

    def move_equip_to_inventory(self, target_item):
        target_slot = self.page.inventories.slots.get(target_item.name)
        if self.moved_slot is not None and target_slot is not None:
            if target_slot.content is not None:
                if self.moved_slot.item_type == target_slot.content.item_type:
                    self.swap_slot(target_slot)

    def move_inventory_to_equit(self, target_item):
        target_slot = self.page.equipments.slots.get(target_item.name)
        if self.moved_slot is not None and target_slot is not None:
            if self.moved_slot.content.item_type == target_slot.item_type:
                with ItemTransactions(self.gameRoot.lengine.the_hero) as trans:
                    state, msg = self.gameRoot.lengine.the_hero.equipment.equip(self.moved_slot)
                    self.page.inventories.update_attr()
                    self.page.equipments.update_attr()

    def move_inventory_to_inventory(self, target_item):
        target_slot = self.page.inventories.slots.get(target_item.name)
        if self.moved_slot is not None and target_slot is not None:
            # if target_slot.content is not None:
                self.swap_slot(target_slot)

    def equip(self, item):
        slot = self.page.inventories.slots.get(item.name)
        if slot is not None:
            if slot.content is not None:
                with ItemTransactions(self.gameRoot.lengine.the_hero) as trans:
                    state, msg = self.gameRoot.lengine.the_hero.equipment.equip(slot)
                    self.page.inventories.update_attr()
                    self.page.equipments.update_attr()

    def unequip(self, item):
        slot = self.page.equipments.slots.get(item.name)
        if slot is not None:
            if slot.content is not None:
                with ItemTransactions(self.gameRoot.lengine.the_hero) as trans:
                    self.gameRoot.lengine.the_hero.equipment.unequip_slot(slot)
                if slot.content is None:
                    item.setPixmapIcon(self.page.equipments.default_icons[item.name])

    def drop_slot(self):
        if self.moved_slot is not None:
            with ItemTransactions(self.gameRoot.lengine.the_hero) as trans:
                self.moved_slot.drop()
                self.page.inventories.update_attr()
                self.page.equipments.update_attr()

    def pop_item(self):
        if self.moved_slot is not None:
            with ItemTransactions(self.gameRoot.lengine.the_hero) as trans:
                self.moved_slot.pop_item()
                self.page.inventories.update_attr()

    def swap_slot(self, target_slot):
        if self.moved_slot is not None:
            with ItemTransactions(self.gameRoot.lengine.the_hero) as trans:
                state = target_slot.swap_item(self.moved_slot)
                self.page.inventories.update_attr()
                self.page.equipments.update_attr()

    def buy(self, item):
        slot = self.page.shop.slots.get(item.name)
        if slot is not None:
            if slot.content is not None:
                with ItemTransactions(self.gameRoot.lengine.the_hero) as trans:
                    self.gameRoot.game.shop.buy(slot)
                if slot.content is None:
                    self.update_gold_count()
                    self.page.inventories.update_attr()
                    item.setPixmapIcon(self.emty_icon)

    def update_gold_count(self):
        self.page.items['hero_gold_value'].setText(str(self.gameRoot.game.shop.customer.gold))
