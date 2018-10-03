from PySide2 import QtGui, QtWidgets, QtCore
from ui.units import HealthBar, HealthText

class UnitMiddleLayer(QtWidgets.QGraphicsItemGroup):
    def __init__(self, gameconfig):
        super(UnitMiddleLayer, self).__init__()
        self.gameconfig = gameconfig
        self.w, self.h = self.gameconfig.unit_size[0], self.gameconfig.unit_size[1]
        self.unit_hptxts = {}
        self.unit_hps = {}
        self.setUpSelectItem()
        self.level = None

    def setLevel(self, level):
        self.level =  level
        self.level.middleLayer = self


    def setUpSelectItem(self):
        self.select_item = QtWidgets.QGraphicsRectItem()
        self.select_item.setRect(0, 0, self.w, self.h)
        self.select_item.setOpacity(0.5)
        self.select_item.setBrush(QtCore.Qt.red)
        self.addToGroup(self.select_item)

        self.selected_item = QtWidgets.QGraphicsRectItem()
        self.selected_item.setRect(0, 0, self.w, self.h)
        self.selected_item.setOpacity(0.3)
        self.selected_item.setBrush(QtCore.Qt.blue)
        self.selected_item.setVisible(False)
        self.addToGroup(self.selected_item)

    def showSelectedItem(self, x, y):
        self.selected_item.setX(x * self.w)
        self.selected_item.setY(y * self.h)
        self.selected_item.setVisible(True)

    def selectItem(self, x, y):
        self.select_item.setX(x * self.w)
        self.select_item.setY(y * self.h)

    def createHPBar(self, unit):
        hp = HealthBar()
        hp.setBrush(QtCore.Qt.cyan)
        hp.setRect(0, self.h , self.w, 32)
        hp.setPos(unit.pos())
        hp.setHP(100)
        self.unit_hps[unit.uid] = hp
        self.addToGroup(self.unit_hps[unit.uid])

    def createHPText(self, unit):
        hpText = HealthText()
        hpText.setUnitPos(unit.pos())
        self.unit_hptxts[unit.uid] = hpText
        self.addToGroup(self.unit_hptxts[unit.uid])

    def getHPprec(self, unit = None):
        return (unit.health * 100)/unit.max_health

    def createSuppot(self, units_at):
        self.createToolTip()
        for unit in units_at.values():
            self.createHPBar(unit)
            self.createHPText(unit)

    def moveSupport(self, unit):
        self.unit_hptxts[unit.uid].setUnitPos(unit.pos())
        self.unit_hps[unit.uid].setPos(unit.pos())

    def updateSupport(self, unit, amount):
        self.unit_hps[unit.uid].setHP(self.getHPprec(unit))
        self.unit_hptxts[unit.uid].setText(amount)

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

    def showToolTip(self, cell, units_at, units_bf):
        if cell in [unit.worldPos for unit in units_at.values()]:
            if cell in units_bf.keys():
                unit = [unit for unit in units_at.values() if unit.worldPos == cell][0]
                self.tooltip.setPos(unit.pos())
                txt = 'uid = ' + str(unit.uid)
                txt += '\nhp = ' + str(units_bf[cell].health)
                txt += '\nmana = ' + str(units_bf[cell].mana)
                txt += '\nstamina = ' + str(units_bf[cell].stamina)
                self.toolText.setPlainText(txt)
                self.tooltip.setVisible(True)
        else:
            self.tooltip.setVisible(False)

    def removeUnitLayer(self, uid):
        self.removeFromGroup(self.unit_hps[uid])
        del self.unit_hps[uid]
        self.removeFromGroup(self.unit_hptxts[uid])
        del self.unit_hptxts[uid]
