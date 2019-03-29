from PySide2 import QtWidgets
from ui.GamePages.suwidgets.items.on_unit.EquipmentWidget import EquipmentWidget
from ui.GamePages.suwidgets.items.on_unit.InventoryWidget import InventoryWidget
from ui.GamePages.suwidgets.items.on_unit.QuickItems import QuickItems
from ui.GamePages.suwidgets.items.on_unit.ShopWidget import ShopWidget
from ui.GamePages.suwidgets.Layouts import GameGridLayout, GameVBoxLayout


class InventoryGroupsWidget:

    def __init__(self, page):
        self.page = page
        self.cfg = page.gamePages.gameRoot.cfg
        self.the_hero = page.the_hero
        self.widgets = []
        self.testAddItem()
        self.setUpWidgets()

    def setUpWidgets(self):
        layout = GameGridLayout()
        self.inventory = InventoryWidget(page=self.page)
        layout.addItem(self.inventory, 0, 0)
        self.widgets.append(self.inventory)
        # group = self.getInventoryGroup()
        self.equimpment = EquipmentWidget(page=self.page)
        layout.addItem(self.equimpment, 0, 1)
        self.widgets.append(self.equimpment)
        self.quick_items = QuickItems(page=self.page)
        layout.addItem(self.quick_items, 0, 2)
        self.widgets.append(self.quick_items)
        self.shop = ShopWidget(page=self.page)
        layout.addItem(self.shop, 0, 3)
        self.widgets.append(self.shop)
        layout.setGeometry()

    def getInventoryGroup(self):
        group = QtWidgets.QTabWidget(self)
        self.equimpment = EquipmentWidget(page=self.page, parent=group)
        group.addTab(self.equimpment, 'Equipment')
        self.quick_items = QuickItems(page=self.page, parent=group)
        group.addTab(self.quick_items, 'Quick items')
        self.scroll = QtWidgets.QScrollArea(parent=self)
        self.shop = ShopWidget(page=self.page, parent=group)
        self.scroll.setWidget(self.shop)
        group.addTab(self.scroll, 'Shop')
        return group

    def testAddItem(self):
        from cntent.items.std.std_items import axe_ancient, stone_axe_cheap, cuirass_usual, jacket_cheap

        # short_sword.item_type = ItemTypes.WEAPON
        self.the_hero.inventory.add(axe_ancient)
        # leather_outfit.item_type = ItemTypes.BODY_ARMOR
        self.the_hero.inventory.add(stone_axe_cheap)
        # cuirass.item_type = ItemTypes.BODY_ARMOR
        self.the_hero.inventory.add(cuirass_usual)
        self.the_hero.inventory.add(jacket_cheap)
        pass

    def upateSlots(self):
        self.inventory.updateSlots()
        self.equimpment.updateSlots()

    def hide(self):
        for widget in self.widgets:
            widget.hide()

    def show(self):
        for widget in self.widgets:
            widget.show()

    def removeFromScene(self):
        for widget in self.widgets:
            widget.removeFromScene()

    def addToScene(self):
        for widget in self.widgets:
            widget.addToScene()
