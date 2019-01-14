from PySide2 import QtWidgets
from ui.GamePages.suwidgets.items.SlotWidget import SlotWidget


class SlotGroupWidget(QtWidgets.QWidget):

    def __init__(self, page, parent=None, ):
        super(SlotGroupWidget, self).__init__(parent)
        self.page = page
        self.type = None
        self.cfg = page.gamePages.gameRoot.cfg
        self.the_hero = page.the_hero
        # self.slot_style = 'background-color:rgba(127, 127, 127, 100);'
        self.slots = dict()

    def setUpWidgets(self):
        pass

    def getSlotWiget(self, game_slot, name, w = 64, h = 64):
        slot = SlotWidget(name, page=self.page, type=self.type, parent=self)
        slot.hovered.connect(self.toolTipShow)
        slot.hover_out.connect(self.page.toolTipHide)
        slot.setProperty('item_type', game_slot.item_type)
        slot.name = name
        slot.setProperty('slot', game_slot)
        # slot.setStyleSheet(self.slot_style)
        slot.setFixedSize(w, h)
        self.slots[game_slot.name] = slot
        return slot

    def setPicSlot(self, game_slot, slot):
        pixmap = self.cfg.getPicFile('slot.png', 101005001)
        slot.empty_pix = pixmap
        if game_slot.content is not None:
            pixmap = self.cfg.getPicFile(game_slot.content.icon, 101005001)
        slot.setPixmap(pixmap)

    def getStyleSlot(self, slot):
        pic_path = self.cfg.pic_file_paths.get('slot.png')
        if slot.content is not None:
            pic_path = self.cfg.pic_file_paths.get(slot.content.icon.lower())
        return "background-image: url('" + pic_path + "');"

    def toolTipShow(self, widget):
        pos = self.parent().parent().mapToParent(widget.pos())
        x, y = pos.x(), pos.y()
        self.page.gamePages.toolTip.setPos(x, y)
        if widget.property('slot').content is None:
            self.page.gamePages.toolTip.setText('Slot empty')
        else:
            self.page.gamePages.toolTip.setDict(widget.property('slot').tooltip_info)
        self.page.gamePages.toolTip.show()
        pass

    def updateWidget(self):
        for slot in self.slots.values():
            self.updateSlot(slot)

    def updateSlot(self, slot):
        self.setPicSlot(slot.property('slot'), slot)

    # def mousePressEvent(self, event):
    #     print(event)

