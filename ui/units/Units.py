from PySide2 import QtWidgets


class Units(QtWidgets.QGraphicsItemGroup):
    def __init__(self, *arg):
        super(Units, self).__init__(*arg)
        self.active_unit = None
        self.units_at = {}
        self.level = None

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
        print('diead')
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

    def unitMoveSlot(self, msg):
        self.level.gameRoot.cfg.sound_maps[msg.get('unit').sound_map.move.lower()].play()
        self.moveUnit(msg.get('unit'), msg.get('cell_to'))
        self.level.middleLayer.moveSupport(self.units_at[msg.get('unit').uid])

    def unitTurnSlot(self, msg):
        self.turnUnit(msg.get('uid'), msg.get('turn'))

    def targetDamageSlot(self, msg):
        # Требуется рефакторинг метод срабатывает после смерти юнита
        if msg.get('target').uid in self.units_at.keys():
            self.level.middleLayer.updateSupport(msg.get('target'), msg.get('amount'))
            self.level.gameRoot.cfg.sound_maps[msg.get('damage_type')].play()
            # print('debug -> damage_type', msg.get('damage_type'))
        pass

    def targetDamageHitSlot(self, msg):
        self.level.gameRoot.cfg.sound_maps[msg.get('sound')].play()

    def attackSlot(self, msg):
        # self.gameRoot.gamePages.gameMenu.showNotify(msg.get('msg'))
        self.level.gameRoot.cfg.sound_maps[msg.get('sound')].play()

    def unitDiedSlot(self, msg):
        self.level.gameRoot.gamePages.gameMenu.rmToUnitStack(msg.get('unit').uid)
        self.level.gameRoot.cfg.sound_maps[msg.get('sound')].play()
        self.level.middleLayer.removeUnitLayer(msg.get('unit').uid)
        self.unitDied(msg.get('unit'))