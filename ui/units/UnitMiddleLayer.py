from PySide2 import QtGui, QtWidgets, QtCore
from ui.units import HealthBar, HealthText
from ui.units.Target import Target

from battlefield import Cell


class UnitMiddleLayer(QtWidgets.QGraphicsItemGroup):
    def __init__(self, gameconfig):
        super(UnitMiddleLayer, self).__init__()
        self.gameconfig = gameconfig
        self.w, self.h = self.gameconfig.unit_size[0], self.gameconfig.unit_size[1]
        self.unit_hptxts = {}
        self.unit_hps = {}
        self.setUpSelectItem()
        self.level = None
        self.targeted = False

    def setLevel(self, level):
        self.level =  level
        self.level.middleLayer = self

    def setUp(self):
        self.level.gameRoot.pages.gameMenu.actives.setTargets.connect(self.getTargets)

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
        if self.targeted:
            self.removeTargets()

    def selectItem(self, x, y):
        self.select_item.setX(x * self.w)
        self.select_item.setY(y * self.h)

    def createHPBar(self, unit, unit_bf):
        hp = HealthBar()
        hp.setBrush(QtCore.Qt.cyan)
        hp.setRect(0, self.h, self.w, 32)
        hp.setPos(unit.pos())
        hp.setHP(self.getHPprec(unit_bf))
        self.unit_hps[unit.uid] = hp
        self.addToGroup(self.unit_hps[unit.uid])

    def createHPText(self, unit):
        hpText = HealthText()
        hpText.setUnitPos(unit.pos())
        self.unit_hptxts[unit.uid] = hpText
        self.addToGroup(self.unit_hptxts[unit.uid])

    def getHPprec(self, unit):
        return (unit.health * 100)/unit.max_health

    def createSuppot(self, units_at, units_bf):
        #TODO Refactoring for unit list
        self.createToolTip()
        for unit in units_at.values():
            self.createHPBar(unit, units_bf[unit.worldPos][0])
            self.createHPText(unit)

    def moveSupport(self, unit):
        self.unit_hptxts[unit.uid].setUnitPos(unit.pos())
        # self.unit_hps[unit.uid].setPos(unit.pos())
        self.update_gui_support(unit)

    def update_gui_support(self, unit):
        self.unit_hps[unit.uid].setScale(unit.scale())
        self.unit_hps[unit.uid].setPos(unit.pos())
        if unit.offset().x() != 0.:
            m = unit.offset().x() / 20
            self.unit_hps[unit.uid].moveBy(unit.offset().x() - m*10, unit.offset().y() - m*10)
        pass

    def updateSupport(self, unit, amount):
        self.unit_hps[unit.uid].setHP(self.getHPprec(unit))
        self.unit_hptxts[unit.uid].setText(amount)

    def createToolTip(self):
        self.tool = self.level.gameRoot.suwidgetFactory.getToolTip(self.w, self.h)
        self.addToGroup(self.tool)

    def showToolTip(self, cell, units_at, units_bf):
        #TODO This method view one unit info from cell, in cell maybe many units
        if cell in [unit.worldPos for unit in units_at.values()]:
            if cell in units_bf.keys():
                unit = [unit for unit in units_at.values() if unit.worldPos == cell][0]
                self.tool.setPos(unit.pos())
                self.tool.setDict(units_bf[cell][0].tooltip_info)
                self.tool.setVisible(True)
        else:
            self.tool.setVisible(False)

    def removeUnitLayer(self, uid):
        self.removeFromGroup(self.unit_hps[uid])
        del self.unit_hps[uid]
        self.removeFromGroup(self.unit_hptxts[uid])
        del self.unit_hptxts[uid]

    def getTargets(self, targets):
        self.targets = []
        for item in targets:
            if isinstance(item, Cell):
                self.addTarget(item)
            else:
                self.addTarget(self.level.gameRoot.game.battlefield.unit_locations[item])

    def addTarget(self, item):
        target = Target()
        target.setBrush(QtCore.Qt.green)
        target.w = self.w
        target.h = self.h
        target.setRect(0, 0, target.w, target.h)
        target.setWorldPos(item.x, item.y)
        self.targets.append(target)
        self.addToGroup(target)
        self.targeted = True

    def removeTargets(self):
        for item in self.targets:
            self.removeFromGroup(item)
        self.targets = []
        self.targeted = False
