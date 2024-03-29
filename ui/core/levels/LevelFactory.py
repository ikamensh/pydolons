from __future__ import annotations

from ui.world import GameWorld
from ui.world.units import UnitMiddleLayer
from ui.world import GameVision
from ui.world.units.BasicUnit import BasicUnit
from ui.world.units import Units, ObstacleUnit
from ui.core.levels.BaseLevel import BaseLevel
from ui.core.debug.DebugLayer import DebugLayer

from game_objects import battlefield_objects as bf_objs
from game_objects.battlefield_objects import Obstacle

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.core.LEngine import LEngine
    from ui.core.GameRootNode import GameRootNode


class LevelFactory:
    def __init__(self, logicEngine):
        self.LEngine: LEngine = logicEngine
        self.gameRoot: GameRootNode = None
        self.level: BaseLevel = None
        pass

    def setGameRoot(self, gameRoot):
        self.gameRoot = gameRoot

    def getLevel(self):
        self.buildLevel()
        return self.level

    def buildLevel(self):
        self.level = BaseLevel()
        self.gameRoot.setLevel(self.level)
        self.z_values = [i for i in range(self.gameRoot.game.bf.w)]
        self.setUpLevel()

    def saveLevelState(self):
        pass

    def setUpLevel(self):
        self.level.setGameWorld(GameWorld(self.gameRoot.cfg))
        self.level.world.setWorldSize(self.gameRoot.game.bf.w, self.gameRoot.game.bf.h)
        self.level.world.setUpFloors(self.gameRoot.game.bf)

        self.level.setMiddleLayer(UnitMiddleLayer(self.gameRoot.cfg))
        self.level.gameVision = GameVision(self.level)
        self.setUpUnits(self.gameRoot.game.bf)
        self.level.gameRoot.cfg.setWorld(self.level.world)
        self.level.gameRoot.controller.setUp(self.level.world, self.level.units, self.level.middleLayer)
        self.level.gameRoot.controller.register(self.level.gameRoot.controller)
        self.level.gameRoot.controller.register(self.level.middleLayer)
        self.level.gameRoot.controller.tr_support.initLevel(self.level)
        self.level.debugLayer = DebugLayer(self.level)
        self.gameRoot.cfg.resourceConfig.music_maps['dungeon_theme.wav'].play()

    def setUpUnits(self, battlefield):
        self.level.setUnits(Units())
        for unit_pos, units in battlefield.cells_to_objs.items():
            for unit in units:
                if isinstance(unit, bf_objs.Unit):
                    gameUnit = BasicUnit(self.gameRoot.cfg.unit_size[0], self.gameRoot.cfg.unit_size[1], gameRoot=self.gameRoot, unit_bf = unit)
                    gameUnit.setUpAnimation()
                    gameUnit.setWorldPos(unit_pos.x, unit_pos.y)
                    gameUnit.last_pos.setX(gameUnit.x())
                    gameUnit.last_pos.setY(gameUnit.y())
                    self.level.gameRoot.view.mouseMove.connect(gameUnit.mouseMove)
                    self.level.units.addToGroup(gameUnit)
                    self.level.units.units_at[unit.uid] = gameUnit
                elif isinstance(unit, Obstacle):
                    obstacle = ObstacleUnit(self.gameRoot.cfg.unit_size[0],
                                            self.gameRoot.cfg.unit_size[1],
                                            name = unit.name)
                    obstacle.setPixmap(self.gameRoot.cfg.getPicFile(unit.icon))
                    obstacle.setWorldPos(unit_pos.x, unit_pos.y)
                    obstacle.uid = unit.uid
                    self.level.world.addToGroup(obstacle)
                    if obstacle.name == 'Wooden door':
                        self.level.units.units_at[unit.uid] = obstacle
                    self.level.world.obstacles[unit.uid] = obstacle
        self.level.units.active_unit = self.level.units.units_at[self.gameRoot.game.turns_manager.get_next().uid]
        self.level.units.update_heaps()
        self.level.units.updateVision()

    def addLevelToScene(self, scene):
        scene.addItem(self.level.world)
        scene.addItem(self.level.units)
        scene.addItem(self.level.gameVision)
        scene.addItem(self.level.middleLayer)
        # scene.addItem(self.level.debugLayer)

    def removeLevelFromScene(self, scene):
        scene.removeItem(self.level.world)
        scene.removeItem(self.level.units)
        scene.removeItem(self.level.middleLayer)
        scene.removeItem(self.level.gameVision)

    def removeLevel(self):
        print('level --destroy')
        self.gameRoot.cfg.resourceConfig.music_maps['dungeon_theme.wav'].stop()
        self.gameRoot.controller.un_register(self.gameRoot.controller)
        self.gameRoot.controller.un_register(self.level.middleLayer)
        self.gameRoot.level = None
        self.gameRoot.controller.tr_support.level = None
        self.level.world.level = None
        self.level.world = None
        self.level.units.destroy()
        # self.level.units = None
        self.level.middleLayer.level = None
        self.level.middleLayer = None
        del self.level




