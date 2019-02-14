from ui.GamePages.suwidgets.items.SlotWidget import SlotWidget
from PySide2 import QtCore


class SlotGroupWidget:

    def __init__(self, page):
        self.page = page
        self.slot_type = None
        self.cfg = page.gamePages.gameRoot.cfg
        self.the_hero = page.the_hero
        # self.slot_style = 'background-color:rgba(127, 127, 127, 100);'
        self.layout = None
        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0
        self._spacing = 5
        self.slots = dict()

    def setUpWidgets(self):
        pass

    def getSlotWidget(self, game_slot, name, w = 64, h = 64):
        slot = SlotWidget(name, page=self.page, slot_type=self.slot_type)
        slot.hovered.connect(self.toolTipShow)
        slot.hover_out.connect(self.page.toolTipHide)
        slot.setProperty('item_type', game_slot.item_type)
        slot.name = name
        slot.setProperty('slot', game_slot)
        self.slots[name] = slot
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

    def toolTipShow(self, slot):
        self.page.gamePages.toolTip.setPos(slot.pos().x(), slot.pos().y())
        if slot.property('slot').content is None:
            self.page.gamePages.toolTip.setText('Slot empty')
        else:
            self.page.gamePages.toolTip.setDict(slot.property('slot').tooltip_info)
        self.page.gamePages.toolTip.show()
        pass

    def updateSlots(self):
        for slot in self.slots.values():
            slot.update_slot()

    # def mousePressEvent(self, event):
    #     print(event)

    def removeFromScene(self):
        for slot in self.slots.values():
            self.page.gamePages.gameRoot.scene.removeItem(slot)
        pass

    def addToScene(self):
        for slot in self.slots.values():
            self.page.gamePages.gameRoot.scene.addItem(slot)
            # slot.installEventFilter(slot)
        pass

    def hide(self):
        for slot in self.slots.values():
            slot.hide()

    def show(self):
        for slot in self.slots.values():
            slot.show()

    def setLayout(self, layout):
        layout.setPos(self._x, self._y)
        layout.setGeometry()
        self.layout = layout

    def sizeHint(self, *args):
        if self.layout is None:
            return QtCore.QSize(0, 0)
        else:
            return self.layout.sizeHint()

    def setPos(self, x, y):
        self._x, self._y = x, y
        if self.layout is not None:
            self.layout.setPos(self._x, self._y)
            self.layout.setGeometry()
        pass

    def pos(self):
        return self._x, self._y

