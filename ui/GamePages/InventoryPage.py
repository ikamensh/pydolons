from PySide2 import QtCore, QtWidgets

from game_objects.items import ItemTransactions, Slot, Equipment, Slot, EquipmentSlotUids


from ui.GamePages import AbstractPage
from ui.GamePages.suwidgets.items.InventoryGroupsWidget import InventoryGroupsWidget


class InventoryPage(AbstractPage):
    def __init__(self, gamePages):
        super(InventoryPage, self).__init__(gamePages)
        self.w, self.h = 700, 550
        self.the_hero = self.gamePages.gameRoot.lengine.the_hero
        self.setUpWidgets()

    def setUpWidgets(self):
        self.background = QtWidgets.QGraphicsPixmapItem(self.gamePages.gameRoot.cfg.getPicFile('arena.jpg'))
        self.resizeBackground(self.background)
        self.addToGroup(self.background)
        mainWidget = InventoryGroupsWidget(page=self)
        self.mainWidget = self.gamePages.gameRoot.scene.addWidget(mainWidget)
        self.mainWidget.widget().setParent(self.gamePages.gameRoot.ui)
        self.mainWidget.widget().hide()
        self.mainWidget.setAcceptDrops(True)
        self.mainWidget.setFlags(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)

        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        self.resized()

    def resized(self):
        super().resized()
        # self.w = self.mainWidget.widget().width()
        # self.h = self.mainWidget.widget().height()
        self.widget_pos.setX(0)
        self.widget_pos.setY(0)

        # self.widget_pos.setX((self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2)
        # self.widget_pos.setY((self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2)
        self.mainWidget.setPos(self.gamePages.gameRoot.view.mapToScene(self.widget_pos))
        self.resizeBackground(self.background)
        pass

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_I:
            if self.state:
                self.hidePage()
            else:
                self.showPage()

    def showPage(self):
        self.state = True
        self.gamePages.page = self
        self.gamePages.visiblePage = True
        self.gamePages.gameRoot.scene.addItem(self)
        self.gamePages.gameRoot.scene.addItem(self.mainWidget)
        self.mainWidget.widget().show()

    def hidePage(self):
        self.state = False
        self.gamePages.page = self.gamePages.gameMenu
        self.gamePages.visiblePage = False
        self.gamePages.gameRoot.scene.removeItem(self)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        self.mainWidget.widget().hide()

    def updatePos(self):
        super().updatePos()
        self.mainWidget.setPos(self.gamePages.gameRoot.view.mapToScene(self.widget_pos))

    def toolTipShow(self, widget):
        x = widget.x() + self.mainWidget.pos().x()
        y = widget.y() + self.mainWidget.pos().y()
        self.gamePages.toolTip.setPos(x, y)
        self.gamePages.toolTip.setText(widget.property('info')(widget))
        self.gamePages.toolTip.show()
        pass

    def toolTipHide(self, widget):
        self.gamePages.toolTip.hide()
        pass

    def equip(self, game_slot):
        with ItemTransactions(self.the_hero) as trans:
            self.the_hero.equipment.equip(game_slot)

        print(self.the_hero.equipment.all_slots)

    def slot_change(self, source, target):
        print('Start trasaction')
        print('source = ', source.property('slot'))
        print('target = ', target.property('slot'))

        if source.property('slot').content is None:
            return

        print('source_IT = ', source.property('slot').content.item_type)
        print('target_IT = ', target.property('slot').item_type)

        with ItemTransactions(self.the_hero) as trans:
            source.property('slot').swap_item(target.property('slot'))

        print(self.the_hero.equipment[EquipmentSlotUids.HANDS])
        print('Equipments ---> ', self.the_hero.equipment.all_items)
        print('inventorys --->', self.the_hero.inventory.all_items)
