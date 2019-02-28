from PySide2 import QtWidgets
from ui.GamePages.suwidgets.items.on_unit.SlotGroupWidget import SlotGroupWidget
from game_objects.items.on_unit.EquipmentSlotUids import EquipmentSlotUids
from ui.GamePages.suwidgets.items.GropsTypes import GropusTypes
from ui.GamePages.suwidgets.Layouts import GameGridLayout


class EquipmentWidget(SlotGroupWidget):

    def __init__(self, page):
        super(EquipmentWidget, self).__init__(page=page)
        self.slot_type = GropusTypes.EQUIPMENT
        self.setUpWidgets()

    def setUpWidgets(self):
        layout = GameGridLayout()
        # print(self.the_hero.equipment.all_slots)
        for game_slot in self.the_hero.equipment.all_slots:
            if game_slot.name == EquipmentSlotUids.HEAD.name:
                slot = self.getSlotWidget(game_slot, game_slot.name)
                self.setPicSlot(game_slot, slot)
                layout.addItem(slot, 0, 2)
            elif game_slot.name == EquipmentSlotUids.BODY.name:
                slot = self.getSlotWidget(game_slot, game_slot.name, h = 128)
                self.setPicSlot(game_slot, slot)
                layout.addItem(slot, 1, 2)
            elif game_slot.name == EquipmentSlotUids.RING_1.name:
                slot = self.getSlotWidget(game_slot, game_slot.name)
                self.setPicSlot(game_slot, slot)
                layout.addItem(slot, 1, 0)
            elif game_slot.name == EquipmentSlotUids.RING_2.name:
                slot = self.getSlotWidget(game_slot, game_slot.name)
                self.setPicSlot(game_slot, slot)
                layout.addItem(slot, 1, 4)
            elif game_slot.name == EquipmentSlotUids.HANDS.name:
                slot_l = self.getSlotWidget(game_slot, game_slot.name + '_l', h = 128)
                self.setPicSlot(game_slot, slot_l)
                layout.addItem(slot_l, 1, 1)
                slot_r = self.getSlotWidget(game_slot, game_slot.name + '_r', h = 128)
                self.setPicSlot(game_slot, slot_r)
                layout.addItem(slot_r, 1, 3)
                slot_l.setProperty('hand', slot_r)
                slot_r.setProperty('hand', slot_l)
            elif game_slot.name == EquipmentSlotUids.FEET.name:
                slot = self.getSlotWidget(game_slot, game_slot.name, h = 128)
                self.setPicSlot(game_slot, slot)
                layout.addItem(slot, 3, 2)

        self.setLayout(layout)
