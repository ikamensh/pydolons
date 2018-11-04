from PySide2 import QtCore, QtGui, QtWidgets

from ui.gamecore.GameObject import GameObject
from ui.GamePages.suwidgets.GuiConsole import GuiConsole
from ui.GamePages.suwidgets.Actives import Actives
from ui.GamePages import AbstractPage


class GameMenuPage(AbstractPage):
    """docstring for ScreenMenu."""
    def __init__(self, gamePages):
        super(GameMenuPage, self).__init__(gamePages)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        self.gui_console = None


    def showNotify(self, text):
        self.notify.showText(text)

    def setUpGui(self):
        self.actives = Actives(self, columns = 6)
        self.actives.setTargets.connect(self.gamePages.gameRoot.level.middleLayer.getTargets)

        self.notify = self.gamePages.gameRoot.suwidgetFactory.getNotifyText(self.gamePages.gameRoot)
        self.addToGroup(self.notify)

        self.unitStack = QtWidgets.QGraphicsRectItem(self)
        self.unitStack.setBrush(QtCore.Qt.blue)
        self.unitStack.setPos(0, 0)

        self.active_select = GameObject()
        self.active_select.setPixmap(self.gamePages.gameRoot.cfg.getPicFile('active select 96.png').scaled(64, 64))
        self.active_select.setParentItem(self.unitStack)
        self.active_select.setPos(self.unitStack.x(), self.unitStack.y())

        if not self.gamePages.gameRoot.level is None:
            self.createUnitStack()
            self.updateUnitStack()

        self.createToolTip()
        self.actives.setScene(self.gamePages.gameRoot.scene)
        print(self.hasFocus())


    def createUnitStack(self):
        self.unitStack.items = {}
        i = 0
        for unit in self.gamePages.gameRoot.level.units.units_at.values():
            item = GameObject(64, 64)
            item.setParentItem(self.unitStack)
            item.setPixmap(unit.pixmap().scaled(64, 64))
            item.setPos(self.unitStack.x() + i* 64, self.unitStack.y())
            item.stackBefore(self.active_select)
            self.unitStack.items[unit.uid] = item
            i+=1

    def createToolTip(self):
        self.tool:QtWidgets.QGraphicsItem = self.gamePages.gameRoot.suwidgetFactory.getToolTip(128, 128)
        self.tool.setVisible(False)
        self.gamePages.gameRoot.scene.addItem(self.tool)

    def showToolTip(self, text, x, y):
        self.tool.setText(text)
        self.tool.setTextPos(x, y)
        self.tool.setVisible(True)

    def hideToolTip(self):
        self.tool.setVisible(False)

    def setUpConsole(self):
        self.gui_console = GuiConsole(self.gamePages.gameRoot.game.gamelog)
        self.gui_console.id = self.gui_console.startTimer(50)
        self.gui_console.setTabChangesFocus(False)
        self.gui_console.setEnabled(False)
        self.gui_console.resize(320, 240)
        self.p_gui_console = self.scene().addWidget(self.gui_console)

    def rmToUnitStack(self, uid):
        self.unitStack.items[uid].setParentItem(None)
        del self.unitStack.items[uid]
        self.updateUnitStack()


    def updateUnitStack(self):
        units_stack = self.gamePages.gameRoot.game.turns_manager.managed_units
        w = len(units_stack)
        self.unitStack.rect().setWidth(w * 64)
        i = 0
        #next_unit = my_context.the_game.turns_manager.get_next()
        for bf_unit in units_stack:
            self.unitStack.items[bf_unit.uid].setPos(self.unitStack.x() + i * 64, self.unitStack.y())
            i+=1

    def setDefaultPos(self):
        pos = self.scene().views()[0].mapToScene(self.gamePages.gameRoot.cfg.correct_size[0], self.gamePages.gameRoot.cfg.correct_size[1])
        self.gui_console.move(self.console_pos[0] + pos.x(), self.console_pos[1] + pos.y())
        self.setX(pos.x())
        self.setY(pos.y())

    def resized(self):
        self.console_pos = self.gamePages.gameRoot.cfg.dev_size[0] - 320, self.gamePages.gameRoot.cfg.dev_size[1] - 240
        self.gui_console.move(self.gamePages.gameRoot.cfg.dev_size[0] - 320, self.gamePages.gameRoot.cfg.dev_size[1] - 240)
        self.actives.resized()

    def mouseMoveEvent(self, e):
        self.actives.mouseMoveEvent(e)

    def destroy(self):
        self.actives.destroy()
        del self.actives
        self.gui_console.killTimer(self.gui_console.id)
        self.gamePages.gameRoot.scene.removeItem(self.p_gui_console )
        del self.p_gui_console
        # self.notify

