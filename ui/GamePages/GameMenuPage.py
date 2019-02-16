from PySide2 import QtCore, QtWidgets

from ui.gamecore.GameObject import GameObject
from ui.GamePages.suwidgets.GuiConsole import GuiConsole
from ui.GamePages.suwidgets.Actives import Actives
from ui.GamePages.suwidgets.SupportPanel import SupportPanel
from ui.GamePages import AbstractPage


class GameMenuPage(AbstractPage):
    """docstring for ScreenMenu."""
    def __init__(self, gamePages):
        super(GameMenuPage, self).__init__(gamePages)
        self.gui_console = None
        self.gamePages.gameRoot.view.wheel_change.connect(self.updatePos)

    def showNotify(self, text):
        self.gamePages.notify.showText(text)

    def setUpGui(self):
        self.actives = Actives(self, columns=6)
        self.actives.setTargets.connect(self.gamePages.gameRoot.level.middleLayer.getTargets)

        self.gamePages.gameRoot.controller.mouseMove.connect(self.actives.mouseMoveEvent)

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

        sup_panel = SupportPanel(page=self, gameconfig=self.gamePages.gameRoot.cfg)
        sup_panel.setUpWidgets()
        self.sup_panel = self.gamePages.gameRoot.scene.addWidget(sup_panel)
        self.sup_panel.setFlags(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)

    def createUnitStack(self):
        self.unitStack.items = {}
        i = 0
        for unit in self.gamePages.gameRoot.level.units.units_at.values():
            item = GameObject(64, 64)
            item.setParentItem(self.unitStack)
            item.setPixmap(unit.pixmap().scaled(64, 64))
            item.setPos(self.unitStack.x() + i * 64, self.unitStack.y())
            item.stackBefore(self.active_select)
            self.unitStack.items[unit.uid] = item
            i += 1

    def toolTipHide(self, widget):
        self.gamePages.toolTip.hide()

    def setUpConsole(self):
        self.gui_console = GuiConsole(self.gamePages.gameRoot.game.gamelog)
        self.gui_console.id = self.gui_console.startTimer(50)
        self.gui_console.setTabChangesFocus(False)
        self.gui_console.resize(320, 240)
        self.gamePages.gameRoot.controller.mouseMove.connect(self.gui_console.setMousePos)
        self.gui_console.btn.clicked.connect(self.updateGuiConsolePos)
        self.p_gui_console = self.scene().addWidget(self.gui_console)
        self.p_gui_console.setFlags(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)

    def updateGuiConsolePos(self):
        self.p_gui_console.setPos(self.gamePages.gameRoot.view.mapToScene(self.gui_console.widget_pos))

    def rmToUnitStack(self, uid):
        self.unitStack.items[uid].setParentItem(None)
        del self.unitStack.items[uid]
        self.updateUnitStack()

    def updateUnitStack(self):
        units_stack = self.gamePages.gameRoot.game.turns_manager.managed_units
        w = len(units_stack)
        self.unitStack.rect().setWidth(w * 64)
        i = 0
        for bf_unit in units_stack:
            self.unitStack.items[bf_unit.uid].setPos(self.unitStack.x() + i * 64, self.unitStack.y())
            i += 1

    def setDefaultPos(self):
        # TODO setDefaultPos is deprecated method, delete in future.
        pos = self.scene().views()[0].mapToScene(self.gamePages.gameRoot.cfg.correct_size[0], self.gamePages.gameRoot.cfg.correct_size[1])
        self.gui_console.move(self.gui_console.x() + pos.x(), self.gui_console.y() + pos.y())
        self.setX(pos.x())
        self.setY(pos.y())

    def resized(self):
        super().resized()
        self.gui_console.resized(self.gamePages.gameRoot.cfg.dev_size)

        self.updateGuiConsolePos()
        self.actives.resized()
        self.upateActivesPos()

    def isFocus(self):
        return self.actives.isFocus() or self.gui_console.isFocus()

    def destroy(self):
        self.gamePages.gameRoot.view.wheel_change.disconnect(self.updatePos)
        self.actives.destroy()
        del self.actives
        self.gui_console.killTimer(self.gui_console.id)
        self.gamePages.gameRoot.scene.removeItem(self.p_gui_console)
        del self.p_gui_console
        self.gamePages.gameRoot.scene.removeItem(self.sup_panel)
        del self.sup_panel

    def updatePos(self):
        super().updatePos()
        self.upateActivesPos()
        self.updateGuiConsolePos()
        self.updadteSupPanlePos()

    def upateActivesPos(self):
        self.actives.mainWidget.setPos(self.gamePages.gameRoot.view.mapToScene(self.actives.x, self.actives.y))

    def updadteSupPanlePos(self):
        self.sup_panel.setPos(self.gamePages.gameRoot.view.mapToScene(self.sup_panel.widget().widget_x, \
                                                                      self.sup_panel.widget().widget_y))



