from __future__ import annotations

from PySide2 import QtWidgets
from ui.world.units.UnitsHeap import UnitsHeap

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.core.levels import BaseLevel
    from ui.world.units.BasicUnit import BasicUnit
    from game_objects.battlefield_objects import Unit


class Units(QtWidgets.QGraphicsItemGroup):
    def __init__(self, *arg):
        super(Units, self).__init__(*arg)
        self.active_unit: BasicUnit = None
        self.units_at = {}
        self.units_pos = {}
        self.groups_at = {}
        self.units_heaps = {}
        self.level: BaseLevel = None
        self.acceptHoverEvents()

    def setLevel(self, level):
        self.level = level
        self.level.units = self
        self.setUpCorpse()

    def setUpCorpse(self):
        self.default_pic_corpse = self.level.gameRoot.cfg.getPicFile('corpse.jpg')
        self.corpse_scale = 0.5

    def getUitsLocations(self):
        for uid, unit in self.units_at.items():
            if uid != self.active_unit.uid:
                yield unit.getWorldPos()

    def moveUnit(self, unit, cell_to):
        if unit == self.level.gameRoot.game.the_hero:
            self.updateVision()
        else:
            self.update_vision_unit(unit, self.level.gameVision.seens)
        print('unit.cell == cell_to', unit.cell == cell_to)
        print('unit.cell, cell_to', unit.cell, cell_to)

        if cell_to not in self.level.world.walls:
            x, y = cell_to.x, cell_to.y
            self.units_at[unit.uid].moveTo(x, y)

    def unitDied(self, unit_bf: Unit):
        unit: BasicUnit = self.units_at[unit_bf.uid]
        unit.uid = unit_bf.corpse.uid
        unit.unit_bf = unit_bf.corpse
        self.units_at[unit.uid] = unit
        self.level.gameRoot.gamePages.gameMenu.remove_from_unitsStack(unit_bf.uid)
        del self.units_at[unit_bf.uid]
        unit.setPixmap(self.level.gameRoot.cfg.getPicFile(unit_bf.corpse.icon))
        unit.is_alive = False
        unit.hpBar.hide()
        unit.direction.hide()
        unit.setScale(self.corpse_scale)
        unit.default_scale = self.corpse_scale

    def turnUnit(self, uid, turn):
        if uid == self.level.gameRoot.game.the_hero.uid:
            self.updateVision()
        self.units_at[uid].setDirection(turn)

    def collisionHeorOfUnits(self, x = None, y = None):
        if x is None:
            if not (self.active_unit.worldPos.x, y) in self.getUitsLocations():
                self.active_unit.setWorldY(y)
        elif y is None:
            if not (x, self.active_unit.worldPos.y) in self.getUitsLocations():
                self.active_unit.setWorldX(x)

    def setActiveUnit(self, unit: Unit):
        self.active_unit = self.units_at[unit.uid]

    def unitMoveSlot(self, msg):
        self.level.gameRoot.cfg.sound_maps[msg.get('unit').sound_map.move.lower()].play()
        self.moveUnit(msg.get('unit'), msg.get('cell_to'))
        self.update_heaps()

    def unitTurnSlot(self, msg):
        self.turnUnit(msg.get('uid'), msg.get('turn'))

    def targetDamageSlot(self, msg):
        if msg.get('target').uid in self.units_at.keys():
            self.units_at[msg.get('target').uid].updateSupport(msg.get('target'), msg.get('amount'))
            self.level.gameRoot.cfg.sound_maps[msg.get('damage_type')].play()

    def targetDamageHitSlot(self, msg):
        self.level.gameRoot.cfg.sound_maps[msg.get('sound')].play()

    def attackSlot(self, msg):
        # self.gameRoot.gamePages.gameMenu.showNotify(msg.get('msg'))
        self.level.gameRoot.cfg.sound_maps[msg.get('sound')].play()

    def unitDiedSlot(self, msg):
        self.level.gameRoot.cfg.sound_maps[msg.get('sound')].play()
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
        seens = self.level.gameRoot.game.vision.std_seen_cells(self.level.gameRoot.game.the_hero)
        self.level.gameVision.setSeenCells(seens)
        for cell, units in self.level.gameRoot.game.bf.cells_to_objs.items():
            for unit_bf in units:
                self.update_vision_unit(unit_bf, seens)

    def update_vision_unit(self, unit_bf: Unit, seens):
        unit: BasicUnit = self.units_at.get(unit_bf.uid)
        if unit is not None:
            unit.setVisible(unit_bf.cell in seens)

    def update_heaps(self):
        for cell, units in self.level.gameRoot.game.bf.cells_to_objs.items():
            if len(units) > 1:
                if cell in self.units_heaps.keys():
                    # self.units_heaps[cell].info()
                    self.units_heaps[cell].update_units(list(self.units_from_(units)))
                else:
                    self.units_heaps[cell] = UnitsHeap(gameRoot=self.level.gameRoot)
                    self.level.gameRoot.controller.mouseMove.connect(self.units_heaps[cell].mouseMoveEvent)
                    self.level.gameRoot.controller.mousePress.connect(self.units_heaps[cell].mousePressEvent)
                    self.units_heaps[cell].update_units(list(self.units_from_(units)))
            else:
                if self.units_heaps.get(cell) is not None:
                    self.destroyUnitsHeap(cell)
                if self.units_at.get(units[0].uid) is not None:
                    self.units_at.get(units[0].uid).refresh_scale()

    def units_from_(self, units):
        for unit in units:
            game_unit = self.units_at.get(unit.uid)
            if game_unit is not None:
                yield self.units_at[unit.uid]

    def destroyUnit(self, unit: BasicUnit):
        if not unit.is_obstacle:
            unit.unit_bf = None
            self.level.gameRoot.view.mouseMove.disconnect(unit.mouseMove)

    def destroyUnitsHeap(self, cell):
        self.level.gameRoot.controller.mouseMove.disconnect(self.units_heaps[cell].mouseMoveEvent)
        self.level.gameRoot.controller.mousePress.disconnect(self.units_heaps[cell].mousePressEvent)
        del self.units_heaps[cell]

    def destroy(self):
        self.active_unit = None
        for unit in self.units_at.values():
            self.destroyUnit(unit)
        self.units_at.clear()
        self.units_pos.clear()
        self.groups_at.clear()
        self.units_heaps.clear()
        self.level = None
        self = None

    def keyPressEvent(self, event):
        # print(event)
        return True





