from PySide2 import QtCore

QObject = QtCore.QObject

from ui.gamecore import GameObject
from ui.units import BasicUnit


class UnitsHeap(QObject, GameObject):
    updated_gui = QtCore.Signal(BasicUnit)

    def __init__(self, *arg, parent=None):
        QObject.__init__(self, parent)
        GameObject.__init__(self, *arg)
        self.max_offset = 20
        self.len = 0
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
        if self.units != new_units:
            for u in self.units:
                if not u in new_units:
                    self.reset_gui(u)
            self.units = new_units[:]
            self.units.reverse()
            self.update_gui()

    def info(self):
        print(self.units, 'len:', len(self.units))

    def reset_gui(self, unit):
        unit.setOffset(0., 0.)
        unit.setScale(1.)

    def update_gui(self):
        if self.units == []:
            return
        i = 0
        for unit in self.units:
            unit.setOffset(i * 20., i * 20.)
            unit.setScale(0.5)
            self.updated_gui.emit(unit)
            i += 1




