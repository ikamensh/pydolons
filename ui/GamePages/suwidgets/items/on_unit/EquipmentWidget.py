from PySide2 import QtWidgets
from ui.GamePages.suwidgets.items.on_unit.SlotGroupWidget import SlotGroupWidget
from game_objects.items.on_unit.EquipmentSlotUids import EquipmentSlotUids


class EquipmentWidget(SlotGroupWidget):

    def __init__(self, page, parent):
        super(EquipmentWidget, self).__init__(page=page, parent=parent)
        self.setUpWidgets()

    def setUpWidgets(self):
        layout = QtWidgets.QGridLayout()
        print(self.the_hero.equipment.all_slots)
        for game_slot in self.the_hero.equipment.all_slots:
            if game_slot.name == EquipmentSlotUids.HEAD.name:
                slot = self.getSlotWiget(game_slot, game_slot.name)
                self.setPicSlot(game_slot, slot)
                layout.addWidget(slot, 0, 2)
            elif game_slot.name == EquipmentSlotUids.BODY.name:
                slot = self.getSlotWiget(game_slot, game_slot.name, h = 128)
                self.setPicSlot(game_slot, slot)
                layout.addWidget(slot, 1, 2)
            elif game_slot.name == EquipmentSlotUids.RING_1.name:
                slot = self.getSlotWiget(game_slot, game_slot.name)
                self.setPicSlot(game_slot, slot)
                layout.addWidget(slot, 1, 0)
            elif game_slot.name == EquipmentSlotUids.RING_2.name:
                slot = self.getSlotWiget(game_slot, game_slot.name)
                self.setPicSlot(game_slot, slot)
                layout.addWidget(slot, 1, 4)
            elif game_slot.name == EquipmentSlotUids.HANDS.name:
                slot_l = self.getSlotWiget(game_slot, game_slot.name, h = 128)
                self.setPicSlot(game_slot, slot_l)
                layout.addWidget(slot_l, 1, 1)
                slot_r = self.getSlotWiget(game_slot, game_slot.name, h = 128)
                self.setPicSlot(game_slot, slot_r)
                layout.addWidget(slot_r, 1, 3)
                slot_l.setProperty('hand', slot_r)
                slot_r.setProperty('hand', slot_l)
            elif game_slot.name == EquipmentSlotUids.FEET.name:
                slot = self.getSlotWiget(game_slot, game_slot.name, h = 128)
                self.setPicSlot(game_slot, slot)
                layout.addWidget(slot, 3, 2)

        self.setLayout(layout)
