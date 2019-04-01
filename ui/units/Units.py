from __future__ import annotations

from PySide2 import QtWidgets
from ui.units.UnitsHeap import UnitsHeap

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.levels import BaseLevel
    from ui.units.BasicUnit import BasicUnit


class Units(QtWidgets.QGraphicsItemGroup):
    def __init__(self, *arg):
        super(Units, self).__init__(*arg)
        self.active_unit:BasicUnit = None
        self.units_at = {}
        self.units_pos = {}
        self.groups_at = {}
        self.units_heaps = {}
        self.level:BaseLevel = None
        self.acceptHoverEvents()

    def setLevel(self, level):
        self.level = level
        self.level.units = self

    def getUitsLocations(self):
        for uid, unit in self.units_at.items():
            if uid != self.active_unit.uid:
                yield unit.getWorldPos()

    def moveUnit(self, unit, cell_to):
        if cell_to is not self.level.gameRoot.game.bf.walls.keys():
            x, y = cell_to.x, cell_to.y
            self.units_at[unit.uid].moveTo(x, y)
            if unit == self.level.gameRoot.game.the_hero:
                self.updateVision()

    def unitDied(self, unit_bf):
        unit = self.units_at[unit_bf.uid]
        self.destroyUnit(unit)
        unit.setVisible(False)
        self.removeFromGroup(unit)
        # if unit != self.level.gameRoot.game.the_hero:
        del self.units_at[unit.uid]
        self.update_heaps()
        self.updateVision()

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

    def unitTurnSlot(self, msg):
        self.turnUnit(msg.get('uid'), msg.get('turn'))

    def targetDamageSlot(self, msg):
        # Требуется рефакторинг метод срабатывает после смерти юнита
        if msg.get('target').uid in self.units_at.keys():
            self.units_at[msg.get('target').uid].updateSupport(msg.get('target'), msg.get('amount'))
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
        self.level.gameVision.setSeenCells(self.level.gameRoot.game.vision.std_seen_cells(hero))
        for cell, units in self.level.gameRoot.game.bf.cells_to_objs.items():
            if cell not in self.level.gameRoot.game.vision.std_seen_cells(hero):
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
        for cell, units in self.level.gameRoot.game.bf.cells_to_objs.items():
            if len(units) > 1:
                if cell in self.units_heaps.keys():
                    self.units_heaps[cell].info()
                    self.units_heaps[cell].update_units(list(self.units_from_(units)))
                else:
                    self.units_heaps[cell] = UnitsHeap(gameRoot=self.level.gameRoot)
                    self.level.gameRoot.controller.mouseMove.connect(self.units_heaps[cell].mouseMoveEvent)
                    self.level.gameRoot.controller.mousePress.connect(self.units_heaps[cell].mousePressEvent)
                    self.units_heaps[cell].update_units(list(self.units_from_(units)))
            else:
                if self.units_heaps.get(cell) is not None:
                    self.destroyUnitsHeap(cell)
                unit = self.units_at.get(units[0].uid)
                if unit is not None:
                    if unit.scale != 1.:
                        unit.setScale(1.)
                        unit.setOffset(0., 0.)

    def units_from_(self, units):
        for unit in units:
            yield self.units_at[unit.uid]

    def setUpToolTip(self, item):
        item.hovered.connect(self.toolTipShow)
        item.hover_out.connect(self.toolTipHide)

    def toolTipShow(self, item):
        pos = self.level.gameRoot.tr_support.groupToScene(item)
        self.level.gameRoot.gamePages.toolTip.setPos(pos[0], pos[1])
        units = self.level.gameRoot.game.bf.cells_to_objs.get(item.worldPos)
        if units is not None:
            if len(units) == 1:
                self.level.gameRoot.gamePages.toolTip.setDict(units[0].tooltip_info)
            # else:
            #     for u in units:
            #         if u.uid == self.units_heaps[item.worldPos].units[-1].uid:
            #             self.level.gameRoot.gamePages.toolTip.setDict(u.tooltip_info)
        self.level.gameRoot.gamePages.toolTip.show()
        pass

    def toolTipHide(self):
        self.level.gameRoot.gamePages.toolTip.hide()
        pass

    def destroyUnit(self, unit):
        if not unit.is_obstacle:
            unit.hovered.disconnect(self.toolTipShow)
            unit.hover_out.disconnect(self.toolTipHide)
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




