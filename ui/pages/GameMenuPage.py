from PySide2 import QtCore, QtWidgets

from ui.core.GameObject import GameObject
from ui.pages.widgets.Actives import Actives
from ui.pages.widgets.SupportPanel import SupportPanel
from ui.pages.suwidgets.UnitsStack import UnitsStack
from ui.pages.suwidgets.TextConsole import TextCosole
from ui.pages import AbstractPage


class GameMenuPage(AbstractPage):
    """docstring for ScreenMenu."""
    def __init__(self, gamePages):
        super(GameMenuPage, self).__init__(gamePages)
        self.actives: Actives = None
        self.active_select: GameObject = None
        self.text_console: TextCosole = None
        self.gamePages.gameRoot.view.wheel_change.connect(self.updatePos)

    def showNotify(self, text):
        self.gamePages.notify.showText(text)

    def setUpGui(self):
        self.actives = Actives(self, columns=6)
        self.actives.setTargets.connect(self.gamePages.gameRoot.level.middleLayer.getTargets)

        self.gamePages.gameRoot.controller.mouseMove.connect(self.actives.mouseMoveEvent)

        self.new_units_stack = UnitsStack(self)
        self.addToGroup(self.new_units_stack)

        if not self.gamePages.gameRoot.level is None:
            self.update_unitsStack()

        self.text_console = TextCosole(self.gamePages.gameRoot.game.gamelog)
        self.gamePages.gameRoot.controller.reg_event_obs(self.text_console)
        self.text_console.setPos(1, 256)
        self.addToGroup(self.text_console)

        sup_panel = SupportPanel(page=self, gameconfig=self.gamePages.gameRoot.cfg)
        sup_panel.setUpWidgets()
        self.sup_panel = self.gamePages.gameRoot.scene.addWidget(sup_panel)
        self.sup_panel.setFlags(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        self.updadteSupPanlePos()

    def remove_from_unitsStack(self, uid):
        self.new_units_stack.remove_unit(uid)

    def update_unitsStack(self):
        self.new_units_stack.update_stack(self.gamePages.gameRoot.game.turns_manager.managed_units[:])

    def toolTipHide(self, widget):
        self.gamePages.toolTip.hide()

    def setDefaultPos(self):
        # TODO setDefaultPos is deprecated method, delete in future.
        pos = self.scene().views()[0].mapToScene(self.gamePages.gameRoot.cfg.correct_size[0], self.gamePages.gameRoot.cfg.correct_size[1])
        self.gui_console.move(self.gui_console.x() + pos.x(), self.gui_console.y() + pos.y())
        self.setX(pos.x())
        self.setY(pos.y())

    def resized(self):
        super().resized()
        self.actives.resized()
        self.upateActivesPos()

    def isFocus(self):
        return self.actives.isFocus()

    def destroy(self):
        self.gamePages.gameRoot.view.wheel_change.disconnect(self.updatePos)
        self.actives.destroy()
        del self.actives
        self.gamePages.gameRoot.scene.removeItem(self.sup_panel)
        del self.sup_panel

    def updatePos(self):
        super().updatePos()
        self.upateActivesPos()
        self.updadteSupPanlePos()

    def upateActivesPos(self):
        self.actives.mainWidget.setPos(self.gamePages.gameRoot.view.mapToScene(self.actives.x, self.actives.y))

    def updadteSupPanlePos(self):
        self.sup_panel.setPos(self.gamePages.gameRoot.view.mapToScene(self.sup_panel.widget().widget_x, \
                                                                      self.sup_panel.widget().widget_y))
