from PySide2 import QtCore, QtGui, QtWidgets

from ui.units import GameObject
from GameLog import gamelog

#    ______
#   /     /
#  /_____/
# /
#/

class GuiConsole(QtWidgets.QPlainTextEdit):
    def __init__(self, *args):
        super(GuiConsole, self).__init__(*args)
        self.last_msg = None
        self.setStyleSheet('color: green;')

    def timerEvent(self, e):
        if self.last_msg != gamelog.msg:
            self.last_msg = gamelog.msg
            self.appendPlainText(str(self.last_msg))

class NotifyText(QtWidgets.QGraphicsTextItem):
    def __init__(self):
        super(NotifyText, self).__init__()
        self.w = 320
        self.h = 240
        # self.setOpacity(1.0)
        self.setFont(QtGui.QFont("Times", 48, 10, False))
        self.setDefaultTextColor(QtCore.Qt.blue)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timerSlot)
        self.setPos(-160, -120)
        self.setVisible(False)

    def setText(self, value):
        self.setOpacity(1.0)
        self.setPlainText(str(value))
        self.setVisible(True)
        self.timer.start(500)

    def timerSlot(self):
        self.setOpacity(self.opacity() - 0.1)
        if self.opacity() < 0.3:
            self.setVisible(False)
            self.timer.stop()

class ScreenMenu(QtWidgets.QGraphicsItemGroup):
    """docstring for ScreenMenu."""
    def __init__(self, *arg):
        super(ScreenMenu, self).__init__(*arg)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        self.level = None
        self.gui_console = None
        self.gameconfig = None
        self.setUpNotify()

    def setUpNotify(self):
        self.notify = NotifyText()
        self.addToGroup(self.notify)

    def showNotify(self, text):
        self.notify.setText(text)

    def setUpDefaultPosition(self):
        self.console_pos = self.gameconfig.ava_ha_size[0] - 320, self.gameconfig.ava_ha_size[1] - 240

    def setScene(self, scene):
        scene.addItem(self)
        self.setUpConsole()


    def setGameConfig(self, gameconfig):
        self.gameconfig = gameconfig
        self.setUpDefaultPosition()

    def setUpLevel(self, level):
        self.level = level

    def setUpGui(self, view):
        self.unitStack = QtWidgets.QGraphicsRectItem(self)
        self.unitStack.setBrush(QtCore.Qt.blue)
        self.unitStack.setPos(-300, -178)
        self.active_select = GameObject()
        self.active_select.setPixmap(self.gameconfig.getPicFile('active select 96.png').scaled(64, 64))
        self.active_select.setParentItem(self.unitStack)
        self.active_select.setPos(self.unitStack.x(), self.unitStack.y())
        if not self.level is None:
            self.createUnitStack()

    def createUnitStack(self):
        self.unitStack.items = {}
        i = 0
        for bf_unit in self.level.units.units_stack:
            unit = self.level.units.units_at[bf_unit.uid]
            item = GameObject(64, 64)
            item.setParentItem(self.unitStack)
            item.setPixmap(unit.pixmap().scaled(64, 64))
            item.setPos(self.unitStack.x() + i* 64, self.unitStack.y())
            item.stackBefore(self.active_select)
            self.unitStack.items[unit.uid] = item
            i+=1

    def setUpConsole(self):
        self.gui_console = GuiConsole()
        self.gui_console.startTimer(50)
        self.gui_console.setTabChangesFocus(False)
        self.gui_console.move(self.console_pos[0], self.console_pos[1])
        self.gui_console.setEnabled(False)
        self.gui_console.resize(320, 240)
        self.scene().addWidget(self.gui_console)

    def updateUnitStack(self, uid = None):
        if not uid is None:
            self.unitStack.items[uid].setParentItem(None)
            del self.unitStack.items[uid]
        w = len(self.level.units.units_stack)
        self.unitStack.rect().setWidth(w * 64)
        i = 0
        for bf_unit in self.level.units.units_stack:
            self.unitStack.items[bf_unit.uid].setPos(self.unitStack.x() + i* 64, self.unitStack.y())
            i+=1

    def resize(self, w, h, view):
        x = w - 120
        y = h - 240
        mapPos = view.mapToScene(x, y)

    def setDefaultPos(self):
        pos = self.scene().views()[0].mapToScene(self.gameconfig.correct_size[0], self.gameconfig.correct_size[1])
        self.gui_console.move(self.console_pos[0] + pos.x(), self.console_pos[1] + pos.y())
        self.setX(pos.x())
        self.setY(pos.y())


class MyCursor(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, *arg):
        super(MyCursor, self).__init__()


    def moveCursor(self, newPos):
        self.setX(newPos.x())
        self.setY(newPos.y())