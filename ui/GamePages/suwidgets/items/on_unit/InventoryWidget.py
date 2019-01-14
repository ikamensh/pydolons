from PySide2 import QtWidgets
from ui.GamePages.suwidgets.items.on_unit.SlotGroupWidget import SlotGroupWidget
from ui.GamePages.suwidgets.items.GropsTypes import GropusTypes


class InventoryWidget(SlotGroupWidget):

    def __init__(self, page, parent ):
        super(InventoryWidget, self).__init__(page=page, parent=parent)
        self.type = GropusTypes.INVENTORY
        self.setUpWidgets()

    def setUpWidgets(self):
        columns = 5
        row = 0
        layout = QtWidgets.QGridLayout(self)
        j = 0
        for i, game_slot in enumerate(self.the_hero.inventory):
            label = self.getSlotWiget(game_slot, name = 'slot_' + str(i + 1))
            self.setPicSlot(game_slot, label)
            layout.addWidget(label, row, j)
            j += 1
            if j >= columns:
                j = 0
                row += 1
        self.setLayout(layout)