from PySide2 import QtCore

QObject = QtCore.QObject

from ui.gamecore import GameObject
from ui.units import BasicUnit
from copy import deepcopy, copy


class UnitsHeap(QObject, GameObject):
    def __init__(self, *arg, parent=None):
        QObject.__init__(self, parent)
        GameObject.__init__(self, *arg)
        self.max_offset = 20
        self.len = 0
        self.units = set()
        # self.cell
        pass

    def add(self, unit: BasicUnit):
        self.len += 1
        unit.setOffset(self.len + 10, 0.)
        self.units.add(unit)
        pass

    def remove(self, unit):
        unit.setOffset(0., 0.)
        for u in self.units:
            if u == unit:
                print('remove unit', unit)
        self.units.remove(unit)
        self.len -= 1

    def update(self):
        pass

    def update_units(self, new_units):
        if self.units != new_units:
            diff = self.units.difference(new_units)
            if diff == set():
                for unit in new_units.difference(self.units):
                    self.add(unit)
            else:
                # self.units = new_units
                for unit in diff:
                    self.remove(unit)
                for unit in new_units.difference(self.units):
                    self.add(unit)
        else:
            print('pass update')

    def info(self):
        print(self.units, 'len:', self.len)

