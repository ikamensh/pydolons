from PySide2 import QtWidgets
from ui.GamePages.suwidgets.items.SlotWidget import SlotWidget
from ui.GamePages.suwidgets.items.on_unit.EquipmentWidget import EquipmentWidget


class InventoryWidget(QtWidgets.QWidget):

    def __init__(self, page, parent = None, ):
        super(InventoryWidget, self).__init__(parent)
        self.page = page
        self.cfg = page.gamePages.gameRoot.cfg
        self.the_hero = page.the_hero
        self.testAddItem()
        self.setUpWidgets()

    def setUpWidgets(self):
        layout = QtWidgets.QGridLayout(self)
        bagpack = self.getBagpack()
        layout.addWidget(bagpack, 0, 0)
        group = self.getInventoryGroup()
        layout.addWidget(group, 0, 1)
        self.setLayout(layout)

    def getBagpack(self):
        columns = 5
        row = 0
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(self)

        j = 0
        for i, game_slot in enumerate(self.the_hero.inventory):
            label = SlotWidget()
            label.setText('slot_' + str(i+1))
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
        widget.setLayout(layout)
        return widget

    def getStyleSlot(self, slot):
        pic_path = self.cfg.pic_file_paths.get('slot.png')
        if slot.content is not None:
            pic_path = self.cfg.pic_file_paths.get(slot.content.icon.lower())
        return "background-image: url('" + pic_path + "');"

    def setPicSlot(self, game_slot, slot):
        pixmap = self.cfg.getPicFile('slot.png', 101005001)
        slot.empty_pix = pixmap
        if game_slot.content is not None:
            pixmap = self.cfg.getPicFile(game_slot.content.icon,101005001)
        slot.setPixmap(pixmap)

    def getInventoryGroup(self):
        group = QtWidgets.QTabWidget(self)
        group.addTab(EquipmentWidget(page=self.page, parent=group),'Equipment')
        return group

    def toolTipShow(self, widget):
        x = widget.x() + self.x() + self.page.mainWidget.pos().x()
        y = widget.y() + self.y() + self.page.mainWidget.pos().y()
        self.page.gamePages.toolTip.setPos(x, y)
        if widget.property('slot').content is None:
            self.page.gamePages.toolTip.setText('Slot empty')
        else:
            self.page.gamePages.toolTip.setDict(widget.property('slot').tooltip_info)
        self.page.gamePages.toolTip.show()
        pass

    def testAddItem(self):
        from cntent.items.blueprints.weapons.weapons import short_sword
        from cntent.items.blueprints.armor.body_armor import leather_outfit, cuirass
        from game_objects.items import ItemTypes


        short_sword.item_type = ItemTypes.WEAPON
        self.the_hero.inventory.add(short_sword)
        leather_outfit.item_type = ItemTypes.BODY_ARMOR
        self.the_hero.inventory.add(leather_outfit)
        cuirass.item_type = ItemTypes.BODY_ARMOR
        self.the_hero.inventory.add(cuirass)
        pass
