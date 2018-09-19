from PySide2 import QtGui, QtWidgets, QtCore
from ui.units import GameObject
from ui.gui_util.gamechanel import gamechanel


class GameWorld(QtWidgets.QGraphicsItemGroup):
    """docstring for GameWorld."""
    def __init__(self, gameconfig):
        super(GameWorld, self).__init__()
        self.gameconfig = gameconfig
        self.worldSize = (1, 1)
        self.worldHalfSize = (1, 1)

    def setWorldSize(self, w, h):
        self.worldSize = (w, h)
        self.worldHalfSize = (int(w / 2), int(h / 2))

    def setFloor(self, pixMap):
        w = int(self.worldSize[0]/2)
        h = int(self.worldSize[1]/2)
        self.floors = []
        for i in range(-w, w, 1):
            col = []
            for j in range(-h, h, 1):
                floor = GameObject(self.gameconfig.unit_size[0], self.gameconfig.unit_size[1])
                floor.setPixmap(pixMap)
                floor.setWorldPos(i, j)
                self.addToGroup(floor)
                col.append(floor)
                # self.floors =self.floors +col
            self.floors.append(col)

class HealtBar(QtWidgets.QGraphicsRectItem):
    """docstring for HealtBar."""
    def __init__(self):
        super(HealtBar, self).__init__()
        self.setOpacity(0.6)

    def setHP(self, hp):
        """ По указанным процентам устанавливает длину HealtBar
        делим на 7 частей
        1/7 -- высоты героя
        6/7 -- начало отсчета
        """

        w = int(128 * hp / 100)
        h = 128 / 7
        y = (6 * 128) / 7
        self.rect().setWidth(w)
        self.setRect(0, y, w, h)

class HealtText(QtWidgets.QGraphicsTextItem):
    def __init__(self):
        super(HealtText, self).__init__()
        self.w = 128
        self.h = 128
        # self.setOpacity(1.0)
        self.setFont(QtGui.QFont("Times", 24, 10, False))
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timerSlot)
        self.setVisible(False)

    def setText(self, value):
        self.setOpacity(1.0)
        if value < 0:
            self.setDefaultTextColor(QtCore.Qt.red)
        else:
            self.setDefaultTextColor(QtCore.Qt.green)
        self.setPlainText(str(value))
        self.setVisible(True)
        self.timer.start(500)

    def setUnitPos(self, pos):
        self.setPos(pos.x() + 32, pos.y() - 32)
        # super().setPos(newpos.x() + 32, newpos.x() - 32)

    def timerSlot(self):
        self.setOpacity(self.opacity() - 0.1)
        if self.opacity() < 0.3:
            self.setVisible(False)
            self.timer.stop()




class MidleLayer(QtWidgets.QGraphicsItemGroup):
    """docstring for MidleLayer."""
    def __init__(self, gameconfig):
        super(MidleLayer, self).__init__()
        self.gameconfig = gameconfig
        self.w, self.h = self.gameconfig.unit_size[0], self.gameconfig.unit_size[1]
        self.unit_hptxts = {}
        self.unit_hps = {}
        self.setUpSelectItem()


    def setUpSelectItem(self):
        self.select_item = QtWidgets.QGraphicsRectItem()
        self.select_item.setRect(0, 0, self.w, self.h)
        self.select_item.setOpacity(0.5)
        self.select_item.setBrush(QtCore.Qt.red)
        self.addToGroup(self.select_item)
        #
        self.selected_item = QtWidgets.QGraphicsRectItem()
        self.selected_item.setRect(0, 0, self.w, self.h)
        self.selected_item.setOpacity(0.3)
        self.selected_item.setBrush(QtCore.Qt.blue)
        self.selected_item.setVisible(False)
        self.addToGroup(self.selected_item)

    def showSelectedItem(self, point):
        self.selected_item.setX(point[0] * self.w)
        self.selected_item.setY(point[1] * self.h)
        self.selected_item.setVisible(True)

    def showSelectItem(self, point):
        self.select_item.setX(point[0] * self.w)
        self.select_item.setY(point[1] * self.h)


    def setUpLevel(self, level):
        self.level = level



    def createHPBar(self):
        for unit in self.level.units.units_at.values():
            hp = HealtBar()
            hp.setBrush(QtCore.Qt.cyan)
            hp.setRect(0, self.h , self.w, 32)
            hp.setPos(unit.pos())
            hp.setHP(100)
            self.unit_hps[unit.uid] = hp
            self.addToGroup(self.unit_hps[unit.uid])
        self.createToolTip()
        self.createHPText()

    def createHPText(self):
        for unit in self.level.units.units_at.values():
            hpText = HealtText()
            hpText.setUnitPos(unit.pos())
            self.unit_hptxts[unit.uid] = hpText
            self.addToGroup(self.unit_hptxts[unit.uid])

    def updateHPText(self):
        message = gamechanel.getMessage()
        if message != {} and message['target'].alive:
            unit = self.level.units.units_at[message['target'].uid]
            self.unit_hptxts[unit.uid].setUnitPos(unit.pos())
            self.unit_hptxts[unit.uid].setText(message['amount'])

    def getHPprec(self, unit):
        return (unit.health * 100)/unit.max_health

    def updateHPBar(self):
        for unit in self.level.units.units_at.values():
            self.unit_hps[unit.uid].setHP(self.getHPprec(self.level.units.units_bf[unit.uid]))
            self.unit_hps[unit.uid].setPos(unit.pos())

    def updateSupport(self):
        self.updateHPBar()
        self.updateHPText()


    def createToolTip(self):
        self.tooltip = QtWidgets.QGraphicsRectItem()
        self.tooltip.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.tooltip.setRect(self.w / 2, - self.h / 2, self.w - 32 , self.h - 32)
        self.tooltip.setOpacity(0.7)
        self.toolText = QtWidgets.QGraphicsTextItem()
        self.toolText.setDefaultTextColor(QtCore.Qt.white)
        self.toolText.setFont(QtGui.QFont("Times", 12, 10, False))
        self.toolText.setParentItem(self.tooltip)
        self.toolText.setPos(self.w / 2, -self.h / 2)
        self.tooltip.setVisible(False)
        self.addToGroup(self.tooltip)

    def showToolTip(self, point):
        if point in self.level.units.units_location.keys():
            unit = self.level.units.getUnit(point[0], point[1])
            self.tooltip.setPos(unit.pos())
            txt = 'uid = ' + str(unit.uid)
            txt += '\nhp = ' + str(self.level.units.units_bf[unit.uid].health)
            txt += '\nmana = ' + str(self.level.units.units_bf[unit.uid].mana)
            txt += '\nstamina = ' + str(self.level.units.units_bf[unit.uid].stamina)
            self.toolText.setPlainText(txt)
            self.tooltip.setVisible(True)
        else:
            self.tooltip.setVisible(False)

    def removeUnitLayer(self, uid):
        self.removeFromGroup(self.unit_hps[uid])
        del self.unit_hps[uid]
        self.removeFromGroup(self.unit_hptxts[uid])
        del self.unit_hptxts[uid]
