from ui.GamePages.suwidgets.items.on_unit.SlotGroupWidget import SlotGroupWidget
from ui.GamePages.suwidgets.items.GropsTypes import GropusTypes
from ui.GamePages.suwidgets.Layouts import GameGridLayout


class QuickItems(SlotGroupWidget):

    def __init__(self, page):
        super(QuickItems, self).__init__(page=page)
        self.slot_type = GropusTypes.QUICKITEMS
        self.setUpWidgets()

    def setUpWidgets(self):
        columns = 5
        row = 0
        layout = GameGridLayout()
        j = 0
        for i, game_slot in enumerate(self.the_hero.quick_items):
            label = self.getSlotWidget(game_slot, name='slot_' + str(i + 1))
            self.setPicSlot(game_slot, label)
            layout.addItem(label, row, j)
            j += 1
            if j >= columns:
                j = 0
                row += 1
        self.setLayout(layout)
