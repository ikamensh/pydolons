from PySide2 import QtCore

QObject = QtCore.QObject

from ui.gamecore import GameObject
from ui.units import BasicUnit


class UnitsHeap(QObject, GameObject):
    updated_gui = QtCore.Signal(BasicUnit)

    def __init__(self, *arg, parent=None, gameRoot=None):
        QObject.__init__(self, parent)
        GameObject.__init__(self, *arg)
        self.gameRoot = gameRoot
        self.u_offset = 20.
        self.u_scale = 0.5
        self.unit_w = None
        self.unit_h = None
        self.len = 0
        self.select_unit = None
        self.units = []
        # self.cell
        pass

    def add(self, unit: BasicUnit):
        self.units.append(unit)
        pass

    def remove(self, unit):
        self.units.remove(unit)

    def update(self):
        pass

    def update_units(self, new_units):
        self.setPos(new_units[0].pos().x(), new_units[0].pos().y())
        if self.units != new_units:
            for u in self.units:
                if not u in new_units:
                    self.reset_gui(u)
            self.units = new_units[:]
            self.units.reverse()
            self.update_gui()
            self.units.reverse()

    def info(self):
        print(self.units, 'len:', len(self.units))
        # for u in self.units:
        #     print('u ----- info')
        #     print('pos', u.pos())
        #     print('rect', u.boundingRect())
        #     print('offset', u.offset())

    def reset_gui(self, unit):
        unit.setOffset(0., 0.)
        unit.setScale(1.)

    def update_gui(self):
        if self.units == []:
            return
        i = 0
        self.units_before()
        self.unit_w = self.units[0].boundingRect().width() * self.u_scale
        self.unit_h = self.units[0].boundingRect().height() * self.u_scale
        for unit in self.units:
            unit.setOffset(i * self.u_offset, i * self.u_offset)
            unit.setScale(self.u_scale)
            self.updated_gui.emit(unit)
            i += 1

    def mouseMoveEvent(self, e):
        pos = self.gameRoot.view.mapToScene(e.pos().x(), e.pos().y())
        x = pos.x() - self.gameRoot.controller.tr_support.tr.m31() - self.gameRoot.level.world.pos().x()
        y = pos.y() - self.gameRoot.controller.tr_support.tr.m32() - self.gameRoot.level.world.pos().y()
        if self.pos().x() < x and self.pos().x() + 128 > x and self.pos().y() < y and self.pos().y() + 128 > y:
            unit = self.getTopLayer(x, y)
            if unit is not None:
                if unit != self.select_unit:
                    if self.select_unit is not None:
                        self.select_unit.setScale(0.5)
                        self.updated_gui.emit(self.select_unit)
                    self.select_unit = unit
                    unit.setScale(0.75)
                    self.updated_gui.emit(unit)
        else:
            if self.select_unit is not None:
                self.select_unit.setScale(0.5)
                self.updated_gui.emit(self.select_unit)
        pass

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.MouseButton.RightButton:
            pos = self.gameRoot.view.mapToScene(e.pos().x(), e.pos().y())
            x = pos.x() - self.gameRoot.controller.tr_support.tr.m31() - self.gameRoot.level.world.pos().x()
            y = pos.y() - self.gameRoot.controller.tr_support.tr.m32() - self.gameRoot.level.world.pos().y()
            if self.pos().x() < x and self.pos().x() + 128 > x and self.pos().y() < y and self.pos().y() + 128 > y:
                if self.select_unit is not None:
                    self.units.remove(self.select_unit)
                    self.units.append(self.select_unit)
                    self.units.reverse()
                    self.update_gui()
                    self.units.reverse()

    def units_before(self):
        l = len(self.units)
        i = 0
        for i in range(l - 1):
            self.units[i + 1].stackBefore(self.units[i])

    def getContains(self, x, y):
        for unit in self.units:
            off_x = unit.pos().x() + unit.offset().x()
            off_y = unit.pos().y() + unit.offset().y()
            if off_x < x and x < off_x + self.unit_w and off_y < y and y < off_y + self.unit_h:
                yield unit

    def getTopLayer(self, x, y):
        l = list(self.getContains(x, y))
        if l == []:
            return None
        l.sort(key=self.sort_key)
        return l[0]

    def sort_key(self, unit):
        return unit.offset().x(), unit.offset().y()
        pass

    def getInter(self):
        a = QtCore.QRect(0, 0, 100, 100)
        b = QtCore.QRect(20, 20, 100, 100)
        if a.x() < b.x() or a.y() < b.y():
            print('a of b')
        return True



