from PySide2 import QtWidgets
from ui.GamePages.suwidgets.items.on_unit.EquipmentWidget import EquipmentWidget
from ui.GamePages.suwidgets.items.on_unit.InventoryWidget import InventoryWidget


class InventoryGroupsWidget(QtWidgets.QWidget):

    def __init__(self, page, parent = None, ):
        super(InventoryGroupsWidget, self).__init__(parent)
        self.page = page
        self.cfg = page.gamePages.gameRoot.cfg
        self.the_hero = page.the_hero
        self.testAddItem()
        self.setUpWidgets()

    def setUpWidgets(self):
        layout = QtWidgets.QGridLayout(self)
        self.inventory = InventoryWidget(page=self.page, parent=self)
        layout.addWidget(self.inventory, 0, 0)
        group = self.getInventoryGroup()
        layout.addWidget(group, 0, 1)
        self.setLayout(layout)

    def getInventoryGroup(self):
        group = QtWidgets.QTabWidget(self)
        self.equimpment = EquipmentWidget(page=self.page, parent=group)
        group.addTab(self.equimpment,'Equipment')
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
        self.inventory.updateWidget()
        self.equimpment.updateWidget()
