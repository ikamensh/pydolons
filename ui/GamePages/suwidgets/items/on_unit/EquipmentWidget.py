from PySide2 import QtWidgets, QtCore
from ui.GamePages.suwidgets.items.SlotWidget import SlotWidget
from game_objects.items.on_unit.EquipmentSlotUids import EquipmentSlotUids


class EquipmentWidget(QtWidgets.QWidget):

    def __init__(self, page, parent=None, ):
        super(EquipmentWidget, self).__init__(parent)
        self.page = page
        self.cfg = page.gamePages.gameRoot.cfg
        self.the_hero = page.the_hero
        self.slot_style = 'background-color:rgba(127, 127, 127, 100);'
        self.slots = dict()
        self.setUpWidgets()

    def setUpWidgets(self):
        layout = QtWidgets.QGridLayout()
        print(self.the_hero.equipment.all_slots)
        for game_slot in self.the_hero.equipment.all_slots:
            if game_slot.name.lower() == str(EquipmentSlotUids.HEAD):
                slot = self.getSlotWiget(game_slot, game_slot.name)
                self.setPicSlot(game_slot, slot)
                layout.addWidget(slot, 0, 2)
            elif game_slot.name.lower() == str(EquipmentSlotUids.BODY):
                slot = self.getSlotWiget(game_slot, game_slot.name, h = 128)
                self.setPicSlot(game_slot, slot)
                layout.addWidget(slot, 1, 2)
            elif game_slot.name.lower() == str(EquipmentSlotUids.RING_1):
                slot = self.getSlotWiget(game_slot, game_slot.name)
                self.setPicSlot(game_slot, slot)
                layout.addWidget(slot, 1, 0)
            elif game_slot.name.lower() == str(EquipmentSlotUids.RING_2):
                slot = self.getSlotWiget(game_slot, game_slot.name)
                self.setPicSlot(game_slot, slot)
                layout.addWidget(slot, 1, 4)
            elif game_slot.name.lower() == str(EquipmentSlotUids.HANDS):
                slot = self.getSlotWiget(game_slot, game_slot.name, h = 128)
                self.setPicSlot(game_slot, slot)
                layout.addWidget(slot, 1, 1)
                slot = self.getSlotWiget(game_slot, game_slot.name, h = 128)
                self.setPicSlot(game_slot, slot)
                layout.addWidget(slot, 1, 3)
            elif game_slot.name.lower() == str(EquipmentSlotUids.FEET):
                slot = self.getSlotWiget(game_slot, game_slot.name, h = 128)
                self.setPicSlot(game_slot, slot)
                layout.addWidget(slot, 3, 2)

        self.setLayout(layout)

    def getSlotWiget(self, game_slot, name, w = 64, h = 64):
        slot = SlotWidget(name, parent=self)
        slot.hovered.connect(self.toolTipShow)
        slot.hover_out.connect(self.page.toolTipHide)
        slot.slot_changed.connect(self.page.slot_change)
        slot.setProperty('item_type', game_slot.item_type)
        slot.setProperty('name', game_slot.name)
        slot.setProperty('slot', game_slot)
        slot.setProperty('info', self.info)
        slot.setStyleSheet(self.slot_style)
        slot.setFixedSize(w, h)
        self.slots[game_slot.name] = slot
        return slot

    def setPicSlot(self, game_slot, slot):
        pixmap = self.cfg.getPicFile('slot.png', 101005001)
        slot.empty_pix = pixmap
        if game_slot.content is not None:
            pixmap = self.cfg.getPicFile(game_slot.content.icon,101005001)
        slot.setPixmap(pixmap)

    def info(self, slot):
        if slot.property('slot').content is None:
            return 'Slot empty'
        else:
            return str(slot.property('slot').content)

    def toolTipShow(self, widget):
        pos = self.parent().parent().mapToParent(widget.pos())
        x, y = pos.x(), pos.y()
        self.page.gamePages.toolTip.setPos(x, y)
        self.page.gamePages.toolTip.setText(self.info(widget))
        self.page.gamePages.toolTip.show()
        pass
