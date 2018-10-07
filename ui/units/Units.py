from PySide2 import QtWidgets


class Units(QtWidgets.QGraphicsItemGroup):
    def __init__(self, *arg):
        super(Units, self).__init__(*arg)
        self.active_unit = None
        self.units_at = {}
        self.level = None

# set slots

    def unitDiedSlot(self, msg):
        self.level.gameRoot.gamePages.gameMenu.rmToUnitStack(msg.get('unit').uid)
        self.level.gameRoot.cfg.sound_maps[msg.get('sound')].play()
        self.level.middleLayer.removeUnitLayer(msg.get('unit').uid)
        self.unitDied(msg.get('unit'))


    def setLevel(self, level):
        self.level =  level
        self.level.units = self

    def getUitsLocations(self):
        for uid, unit in self.units_at.items():
            if uid != self.active_unit.uid:
                yield unit.getWorldPos()

    def moveUnit(self, unit, cell_to):
        x, y = cell_to.x, cell_to.y
        self.units_at[unit.uid].setWorldPos(x, y)

    def unitDied(self, unit):
        unit = self.units_at[unit.uid]
        self.removeFromGroup(unit)
        del self.units_at[unit.uid]

    def turnUnit(self, uid, turn):
        self.units_at[uid].setDirection(turn)

    def collisionHeorOfUnits(self, x = None, y = None):
        if x is None:
            if not (self.active_unit.worldPos.x, y) in self.getUitsLocations():
                self.active_unit.setWorldY(y)
                # self.moveUnit(self.active_unit, self.active_unit.worldPos)
        elif y is None:
            if not (x, self.active_unit.worldPos.y) in self.getUitsLocations():
                self.active_unit.setWorldX(x)
                # self.moveUnit(self.active_unit, self.active_unit.worldPos)

    def setActiveUnit(self, unit):
        self.active_unit = self.units_at[unit.uid]
