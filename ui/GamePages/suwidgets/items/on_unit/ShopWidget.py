from ui.GamePages.suwidgets.items.on_unit.SlotGroupWidget import SlotGroupWidget
from ui.GamePages.suwidgets.items.GropsTypes import GropusTypes
from ui.GamePages.suwidgets.Layouts import GameGridLayout


class ShopWidget(SlotGroupWidget):

    def __init__(self, page):
        super(ShopWidget, self).__init__(page=page)
        self.shop = page.gamePages.gameRoot.game.shop
        self.slot_type = GropusTypes.SHOP
        self.setUpWidgets()

    def setUpWidgets(self):
        columns = 3
        row = 0
        layout = GameGridLayout()
        j = 0
        for i, game_slot in enumerate(self.shop.inventory):
            label = self.getSlotWidget(game_slot, name='slot_' + str(i + 1))
            self.setPicSlot(game_slot, label)
            layout.addItem(label, row, j)
            j += 1
            if j >= columns:
                j = 0
                row += 1
        self.setLayout(layout)
        pass

    def addSlot(self):
        pass

    def removeSlot(self):
        pass