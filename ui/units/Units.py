from PySide2 import QtWidgets
from ui.units.UnitsHeap import UnitsHeap


class Units(QtWidgets.QGraphicsItemGroup):
    def __init__(self, *arg):
        super(Units, self).__init__(*arg)
        self.active_unit = None
        self.units_at = {}
        self.units_pos = {}
        self.groups_at = {}
        self.units_heaps = {}
        self.level = None

    def setLevel(self, level):
        self.level = level
        self.level.units = self

    def getUitsLocations(self):
        for uid, unit in self.units_at.items():
            if uid != self.active_unit.uid:
                yield unit.getWorldPos()

    def moveUnit(self, unit, cell_to):
        if unit == self.level.gameRoot.game.the_hero:
            self.updateVision()
        x, y = cell_to.x, cell_to.y
        self.units_at[unit.uid].setWorldPos(x, y)

    def unitDied(self, unit):
        unit = self.units_at[unit.uid]
        self.removeFromGroup(unit)
        if unit != self.level.gameRoot.game.the_hero:
            self.updateVision()
        del self.units_at[unit.uid]

    def turnUnit(self, uid, turn):
        if uid == self.level.gameRoot.game.the_hero.uid:
            self.updateVision()
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
        self.update_heaps()
        self.level.middleLayer.moveSupport(self.units_at[msg.get('unit').uid])

    def unitTurnSlot(self, msg):
        self.turnUnit(msg.get('uid'), msg.get('turn'))

    def targetDamageSlot(self, msg):
        # Требуется рефакторинг метод срабатывает после смерти юнита
        if msg.get('target').uid in self.units_at.keys():
            self.level.middleLayer.updateSupport(msg.get('target'), msg.get('amount'))
            self.level.gameRoot.cfg.sound_maps[msg.get('damage_type')].play()
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

    def addToUnitsGroup(self, unit):
            # group = self.groups_at.get(unit.worldPos)
            # if group is None:
            #     self.groups_at[unit.worldPos] =
            # print('add', unit)
            pass

    def getUnitsFromCell(self, cell_to):
        for unit in self.units_at.values():
            if unit.worldPos == cell_to:
                yield unit

    def updateVision(self):
        hero = self.level.gameRoot.game.the_hero
        bf = self.level.gameRoot.game.battlefield
        self.level.gameVision.setSeenCells(bf.vision.std_seen_cells(hero))
        for cell, units in self.level.gameRoot.game.battlefield.units_at.items():
            if cell not in bf.vision.std_seen_cells(hero):
                for u in units:
                    unit = self.units_at.get(u.uid)
                    if unit is not None:
                        unit.setVisible(False)
            else:
                for u in units:
                    unit = self.units_at.get(u.uid)
                    if unit is not None:
                        unit.setVisible(True)

    def update_heaps(self):
        for cell, units in self.level.gameRoot.game.battlefield.units_at.items():
            if len(units) > 1:
                if cell in self.units_heaps.keys():
                    self.units_heaps[cell].info()
                    self.units_heaps[cell].update_units(list(self.units_from_(units)))
                else:
                    self.units_heaps[cell] = UnitsHeap(gameRoot=self.level.gameRoot)
                    self.level.gameRoot.controller.mouseMove.connect(self.units_heaps[cell].mouseMoveEvent)
                    self.level.gameRoot.controller.mousePress.connect(self.units_heaps[cell].mousePressEvent)
                    self.units_heaps[cell].updated_gui.connect(self.level.middleLayer.update_gui_support)
                    self.units_heaps[cell].update_units(list(self.units_from_(units)))
            elif self.units_at[units[0].uid].scale != 1.:
                    if self.units_heaps.get(cell) is not None:
                        del self.units_heaps[cell]
                    self.units_at[units[0].uid].setScale(1.)
                    self.units_at[units[0].uid].setOffset(0., 0.)
                    self.level.middleLayer.update_gui_support(self.units_at[units[0].uid])

    def units_from_(self, units):
        for unit in units:
            yield self.units_at[unit.uid]



