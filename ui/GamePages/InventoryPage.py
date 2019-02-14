from PySide2 import QtCore, QtWidgets

from game_objects.items import ItemTransactions


from ui.GamePages import AbstractPage
from ui.GamePages.suwidgets.items.InventoryGroupsWidget import InventoryGroupsWidget


class InventoryPage(AbstractPage):
    def __init__(self, gamePages):
        super(InventoryPage, self).__init__(gamePages)
        self.w, self.h = 700, 550
        self.the_hero = self.gamePages.gameRoot.lengine.the_hero
        self.dragSetUp()
        self.setUpWidgets()
        self.state = False

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

    def setUpWidgets(self):
        self.gamePages.gameRoot.scene.addItem(self)
        self.background = QtWidgets.QGraphicsPixmapItem(self.gamePages.gameRoot.cfg.getPicFile('arena.jpg'))
        self.resizeBackground(self.background)

        self.item = QtWidgets.QGraphicsPixmapItem()
        self.gamePages.gameRoot.scene.addItem(self.item)
        self.item.hide()

        self.addToGroup(self.background)
        self.mainWidget = InventoryGroupsWidget(page=self)
        # self.mainWidget = self.gamePages.gameRoot.scene.addWidget(mainWidget)
        # self.mainWidget.widget().setParent(self.gamePages.gameRoot.ui)
        # self.mainWidget.widget().hide()
        # self.mainWidget.setAcceptDrops(True)
        # self.mainWidget.setFlags(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        #
        # self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        self.mainWidget.addToScene()
        self.hidePage()
        self.resized()

    def resized(self):
        super().resized()
        # self.w = self.mainWidget.widget().width()
        # self.h = self.mainWidget.widget().height()
        self.widget_pos.setX(0)
        self.widget_pos.setY(0)

        # self.widget_pos.setX((self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2)
        # self.widget_pos.setY((self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2)
        # self.mainWidget.setPos(self.gamePages.gameRoot.view.mapToScene(self.widget_pos))
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
        self.show()
        self.mainWidget.show()

    def hidePage(self):
        self.state = False
        self.gamePages.page = self.gamePages.gameMenu
        self.gamePages.visiblePage = False
        self.hide()
        self.mainWidget.hide()
        self.deSelectSlot()

    def updatePos(self):
        super().updatePos()
        # self.mainWidget.setPos(self.gamePages.gameRoot.view.mapToScene(self.widget_pos))

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

    def equip(self, slot):
        with ItemTransactions(self.the_hero) as trans:
            state, msg = self.the_hero.equipment.equip(slot.property('slot'))
            if state:
                self.updatePage()
            else:
                self.gamePages.notify.showText(msg)

    def unequip_slot(self, slot):
        with ItemTransactions(self.the_hero) as trans:
            self.the_hero.equipment.unequip_slot(slot.property('slot'))
            self.updatePage()

    def buy(self, slot):
        with ItemTransactions(self.the_hero) as trans:
            self.gamePages.gameRoot.game.shop.buy(slot.property('slot'))
        self.updatePage()

    def drop(self, game_slot):
        with ItemTransactions(self.the_hero) as trans:
            game_slot.drop()
            self.updatePage()

    def updatePage(self):
        self.mainWidget.upateSlots()
        self.update(0, 0, self.gamePages.gameRoot.cfg.dev_size[0],self.gamePages.gameRoot.cfg.dev_size[1])

    def swap_item(self, source, target):
        with ItemTransactions(self.the_hero) as trans:
            state = source.property('slot').swap_item(target.property('slot'))
            source.update_slot()
            target.update_slot()
            if not state:
                self.gamePages.notify.showText('Not add item')
            return state
        return False

    def deSelectSlot(self):
        if self.source is not None:
            self.source.setDefaultStyle()
            self.source.isDown = False
            self.source.isChecked = False
            self.source = None

    def mouseMoveEvent(self, event):
        if self.source is not None:
            pos = self.gamePages.gameRoot.view.mapToScene(event.pos())
            # self.setPos(pos)
            self.item.setX(pos.x() + 10)
            self.item.setY(pos.y() + 10)
        pass

