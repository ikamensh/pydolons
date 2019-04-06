from ui.pages import AbstractPage
from ui.pages.inventory_page.ScrollBlock import ScrollBlock
from ui.pages.inventory_page.GameInventrory import GameInventrory
from ui.pages.inventory_page.GameEquipment import GameEquipment
from ui.pages.inventory_page.GameShop import GameShop
from ui.pages.suwidgets.BaseItem import BaseItem
from ui.pages.inventory_page.SlotMoveMaster import SlotMoveMaster

from PySide2 import QtCore


class InventoryPage(AbstractPage):
    def __init__(self, gamePages):
        super(InventoryPage, self).__init__(gamePages)
        self.readXML('inventory_page.xml')
        self.setUpInventories()
        self.setUpEquipments()
        self.setUpShop()
        self.setUpMoveMaster()
        self.read_tree()
        self.setUpScroll()
        self.setUpSlots()
        self.name = 'inventory_page'
        self._names = ['bug', 'eat', 'bug', 'good']
        self.input = ''
        self.item_hover = None
        # self.setAcceptedMouseButtons(QtCore.Qt.LeftButton | QtCore.Qt.RightButton)
        self.gamePages.gameRoot.view.wheel_change.connect(self.updatePos)

    def dragSetUp(self):
        self.source = None
        self.target = None

    def startManipulation(self, slot):
        if self.source is slot:
            self.source = None
            return
        if self.source is None:
            self.source = slot
            self.item.setPixmap(self.source.pixmap())
            self.item.show()
            self.item.setZValue(150.00)
            return
        else:
            self.target = slot
            self.source.setDefaultStyle()
            self.target.setDefaultStyle()
            self.item.setZValue(0.0)
            self.swap_item(self.source, self.target)
            self.target = None
            self.source = None
            self.item.hide()
        self.updatePage()

    def sceneEvent(self, event:QtCore.QEvent):
        self.update(0, 0, self.gamePages.gameRoot.cfg.dev_size[0], self.gamePages.gameRoot.cfg.dev_size[1])
        # if self.scrollSetEvent(event):
        #     return True
        if event.type() is QtCore.QEvent.GraphicsSceneHoverMove:
            self.hoverMove(self.scene().itemAt(event.scenePos(), self.scene().views()[0].transform()))
            return True
        elif event.type() is QtCore.QEvent.GraphicsSceneContextMenu:
            self.contextMenuEvent(event)
            return True
        elif event.type() is QtCore.QEvent.GraphicsSceneMousePress:
            if event.button() is QtCore.Qt.LeftButton:
                self.mousePressLeft(event)
            return True
        elif event.type() is QtCore.QEvent.GraphicsSceneMouseRelease:
            self.mouseReleaseEvent(event)
            return True
        elif event.type() is QtCore.QEvent.GraphicsSceneMouseMove:
            self.mouseMoveEvent(event)
            return True
        else:
            return super(InventoryPage, self).sceneEvent(event)

    def contextMenuEvent(self, event):
        item = self.scene().itemAt(event.scenePos(), self.scene().views()[0].transform())
        print('contex', item.name)
        if item._names[0] == 'shop':
            self.move_master.buy(item)
        elif item._names[0] == 'inventory':
            self.move_master.equip(item)
        elif item._names[0] == 'equip':
            self.move_master.unequip(item)

    def mousePressEvent(self, event):
        item = self.scene().itemAt(event.scenePos(), self.scene().views()[0].transform())
        if item._names[0] == 'inventory':
            self.moveInventoryItem(item)

    def mouseReleaseEvent(self, event):
        items = self.scene().items(event.scenePos())
        self.drop_slot(items[1])
        self.s_engine_2.mouseReleaseEvent()
        self.s_engine.mouseReleaseEvent()

    def mousePressLeft(self, event):
        item = self.scene().itemAt(event.scenePos(), self.scene().views()[0].transform())
        if item._names[0] == 'inventory':
            self.move_master.moved_slot = self.inventories.getMovedSlot(item)
        elif item._names[0] == 'equip':
            self.move_master.moved_slot = self.equipments.getMovedSlot(item)
        elif item.name == 'shop_scroll_but':
            self.s_engine_2.mousePressEvent(event)
            self.move_master.moved_slot = None
        elif item.name == 'scroll_but':
            self.s_engine.mousePressEvent(event)
            self.move_master.moved_slot = None
        if self.move_master.moved_slot is not None:
            self.moved_slot._names = item._names[:]
            self.moved_slot.name = item.name
            self.moved_slot.isChecked = True

    def mouseMoveEvent(self, event):
        self.s_engine_2.mouseMoveEvent(event)
        self.s_engine.mouseMoveEvent(event)
        self.move_slot(event)

    def hoverMove(self, item):
        if item is not None:
            if item == self.item_hover:
                self.show_info(item)
            else:
                self.item_hover = item

    def show_info(self, item):
        if item._names[0] == 'equip':
            self.show_equipment_info(item)
        elif item._names[0] +'_'+ item._names[1] == 'inventory_slot':
            self.show_inventory_info(item)
        elif item._names[0] +'_'+ item._names[1] == 'shop_slot':
            self.show_shop_info(item)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_I:
            if self.state:
                self.hidePage()
            else:
                self.showPage()

    def showPage(self):
        self.state = True
        self.show()

    def hidePage(self):
        self.state = False
        self.hide()

    ######## S L O T S #############

    def setUpMoveMaster(self):
        self.move_master = SlotMoveMaster(self.gamePages.gameRoot, self)

    def setUpSlots(self):
        self.move_master.update_gold_count()
        self.moved_slot = BaseItem(page=self, parent=self)
        attr = {}
        attr['name'] = 'moved_slot'
        attr['top'] = '0'
        attr['left'] = '0'
        attr['height'] = '128'
        attr['width'] = '128'
        attr['icon'] = 'cha_page_elemnt_bg.png'
        tag = 'item'
        self.moved_slot.setUpAttrib(attr)
        self.moved_slot.hide()
        self.addToGroup(self.moved_slot)

    def move_slot(self, event):
        if self.moved_slot.isChecked:
            self.moved_slot._top = event.pos().y() - 32
            self.moved_slot._left = event.pos().x() - 32
            self.moved_slot.show()

    def drop_slot(self, target):
        self.moved_slot.isChecked = False
        if target._names[1] == 'slot' and self.moved_slot.name != target.name:
            if self.moved_slot._names[0] == 'inventory':
                if target._names[0] == 'inventory':
                    self.move_master.move_inventory_to_inventory(target)
                elif target._names[0] == 'equip':
                    self.move_master.move_inventory_to_equit(target)
            if self.moved_slot._names[0] == 'equip':
                if target._names[0] == 'inventory':
                    self.move_master.move_equip_to_inventory(target)
        else:
            if self.moved_slot._names[0] == 'inventory':
                self.move_master.pop_item()
            # elif self.moved_slot._names[0] == 'equip':
            #     self.equipments.drop_slot()
            #     self.equipments.update_attr()
        self.moved_slot.hide()

    ############ S C R O L L ##############

    def setUpScroll(self):
        self.s_engine = ScrollBlock(self, width=self.items['scroll_block'].width)
        self.s_engine.setScrollBut(self.items['scroll_but'])
        for i in range(self.inventories.len):
            self.s_engine.addScrollItem(self.items['inventory_slot_'+str(i)])

        self.s_engine_2 = ScrollBlock(self, width=self.items['shop_scroll_block'].width)
        self.s_engine_2.setScrollBut(self.items['shop_scroll_but'])
        for i in range(self.shop.len):
            self.s_engine_2.addScrollItem(self.items['shop_slot_' + str(i)])

    def scrollSetEvent(self, event):
        if self.s_engine.setEvent(event, self):
            return True
        elif self.s_engine_2.setEvent(event, self):
            return True
        else:
            return False

    ########### I N V E N T O R Y #############

    def setUpInventories(self):
        self.inventories = GameInventrory(self.gamePages.gameRoot, page=self)
        for element in self.xml_page.iter():
            name = element.get('name')
            if name is not None:
                if name == 'scroll_block':
                    self.inventories.setUpSlots(element)

    def moveInventoryItem(self, item):
        self.inventories.move_item(item)

    def show_inventory_info(self, item):
        slot = self.inventories.slots.get(item.name)
        if slot is not None:
            info = self.setDict(slot.tooltip_info)
            self.items.get('info_value').setText(info)

    ######### E Q U I P M E N T ###############

    def setUpEquipments(self):
        self.equipments = GameEquipment(self.gamePages.gameRoot, self)
        for element in self.xml_page.iter():
            name = element.get('name')
            if name is not None:
                if name == 'equipments_block':
                    self.equipments.setUpSlots(element)

    def show_equipment_info(self, item):
        slot = self.equipments.slots.get(item.name)
        if slot is not None:
            self.items.get('info_value').setText(self.setDict(slot.tooltip_info))

    ############## S H O P ##############

    def setUpShop(self):
        self.shop = GameShop(self.gamePages.gameRoot, page=self)
        for element in self.xml_page.iter():
            name = element.get('name')
            if name is not None:
                if name == 'shop_scroll_block':
                    self.shop.setUpSlots(element)

    def show_shop_info(self, item):
        slot = self.shop.slots.get(item.name)
        if slot is not None:
            self.items.get('info_value').setText(self.setDict(self.shop.show_info(slot)))

