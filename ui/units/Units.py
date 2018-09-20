from PySide2 import QtWidgets

class Units(QtWidgets.QGraphicsItemGroup):
    def __init__(self, *arg):
        super(Units, self).__init__(*arg)
        self.active_unit = None
        self.units_location = {}
        self.units_at = {}
        self.units_bf = {}
        self.units_stack = None


    def getUitsLocations(self):
        for uid, unit in self.units_at.items():
            if uid != self.active_unit.uid:
                yield unit.getWorldPos()

    def getUnit(self, x, y):
        return self.units_location.setdefault((x, y), None)


    def updateLocations(self, unit, pos):
        del self.units_location[pos]
        self.units_location[(unit.worldPos.x(), unit.worldPos.y())] = unit


    def collisionHeorOfUnits(self, x = None, y = None):
        if x is None:
            if not (self.active_unit.worldPos.x(), y) in self.getUitsLocations():
                pos = (self.active_unit.worldPos.x(), self.active_unit.worldPos.y())
                self.active_unit.setWorldY(y)
                self.updateLocations(self.active_unit, pos)
        elif y is None:
            if not (x, self.active_unit.worldPos.y()) in self.getUitsLocations():
                pos = (self.active_unit.worldPos.x(), self.active_unit.worldPos.y())
                self.active_unit.setWorldX(x)
                self.updateLocations(self.active_unit, pos)


    def removeUnit(self, uid):
        unit = self.units_at[uid]
        self.removeFromGroup(unit)
        del self.units_location[(unit.worldPos.x(), unit.worldPos.y())]
        self.locations.remove(unit.worldPos)
        del self.units_bf[uid]
        del self.units_at[uid]


    def setActiveUnit(self, unit):
        self.active_unit = self.units_at[unit.uid]


    def setUnitStack(self, units):
        self.units_stack = units
