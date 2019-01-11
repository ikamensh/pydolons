from PySide2 import QtWidgets
from ui.GamePages.suwidgets.items.SlotWidget import SlotWidget
from ui.GamePages.suwidgets.items.on_unit.SlotGroupWidget import SlotGroupWidget


class InventoryWidget(SlotGroupWidget):

    def __init__(self, page, parent ):
        super(InventoryWidget, self).__init__(page=page, parent=parent)
        self.setUpWidgets()

    def setUpWidgets(self):
        columns = 5
        row = 0
        layout = QtWidgets.QGridLayout(self)

        j = 0
        for i, game_slot in enumerate(self.the_hero.inventory):
            label = SlotWidget()
            label.setText('slot_' + str(i + 1))
            label.hovered.connect(self.toolTipShow)
            label.hover_out.connect(self.page.toolTipHide)
            label.slot_changed.connect(self.page.slot_change)
            label.setFixedSize(64, 64)
            label.setProperty('slot', game_slot)
            self.setPicSlot(game_slot, label)
            layout.addWidget(label, row, j)
            j += 1
            if j >= columns:
                j = 0
                row += 1
        self.setLayout(layout)
