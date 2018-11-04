from ui.GameWorld import GameWorld, ObstacleUnit
from ui.units import UnitMiddleLayer
from ui.units import Units, BasicUnit
from ui.levels.BaseLevel import BaseLevel

from game_objects import battlefield_objects as bf_objs
from game_objects.battlefield_objects import  Obstacle


class LevelFactory:
    def __init__(self, logicEngine):
        self.LEngine = logicEngine
        self.gameRoot = None
        self.level:BaseLevel = None
        pass

    def setGameRoot(self, gameRoot):
        self.gameRoot = gameRoot

    def getLevel(self):
        self.buildLevel()
        return self.level

    def buildLevel(self):
        self.level = BaseLevel()
        self.gameRoot.setLevel(self.level)
        self.z_values = [i for i in range(self.gameRoot.game.battlefield.w)]
        self.setUpLevel()


    def removeLevel(self):
        pass

    def saveLevelState(self):
        pass

    def setUpLevel(self):
        self.level.setGameWorld(GameWorld(self.gameRoot.cfg))
        self.level.world.setWorldSize(self.gameRoot.game.battlefield.w, self.gameRoot.game.battlefield.h)
        self.level.world.setFloor(self.gameRoot.cfg.getPicFile('floor.png'))

        self.level.setMiddleLayer(UnitMiddleLayer(self.gameRoot.cfg))

        self.setUpUnits(self.gameRoot.game.battlefield)
        self.level.gameRoot.cfg.setWorld(self.level.world)
        self.level.gameRoot.controller.setUp(self.level.world, self.level.units, self.level.middleLayer)

    def setUpUnits(self, battlefield):
        self.level.setUnits(Units())
        for unit, unit_pos in battlefield.unit_locations.items():
            if isinstance(unit, bf_objs.Unit):
                gameUnit = BasicUnit(self.gameRoot.cfg.unit_size[0], self.gameRoot.cfg.unit_size[1], gameconfig=self.gameRoot.cfg)
                if unit.icon == 'hero.png':
                    self.active_unit = True
                gameUnit.setPixmap(self.gameRoot.cfg.getPicFile(unit.icon))
                gameUnit.setDirection(battlefield.unit_facings[unit])
                gameUnit.setWorldPos(unit_pos.x, unit_pos.y)
                gameUnit.uid = unit.uid
                self.level.units.addToGroup(gameUnit)
                # добавили gameunit
                self.level.units.units_at[unit.uid] = gameUnit
            elif isinstance(unit, Obstacle):
                obstacle:ObstacleUnit = ObstacleUnit(self.gameRoot.cfg.unit_size[0], self.gameRoot.cfg.unit_size[1])
                obstacle.setPixmap(self.gameRoot.cfg.getPicFile(unit.icon))
                obstacle.setWorldPos(unit_pos.x, unit_pos.y)
                obstacle.uid = unit.uid
                self.level.world.addToGroup(obstacle)
                self.level.world.obstacles[unit.uid] = obstacle

        self.level.units.active_unit = self.level.units.units_at[self.gameRoot.game.turns_manager.get_next().uid]
        self.level.middleLayer.createSuppot(self.level.units.units_at, battlefield.units_at)

    def addLevelToScene(self, scene):
        scene.addItem(self.level.world)
        scene.addItem(self.level.units)
        scene.addItem(self.level.middleLayer)

    def removeLevelFromScene(self, scene):
        scene.removeItem(self.level.world)
        scene.removeItem(self.level.units)
        scene.removeItem(self.level.middleLayer)

    def removeLevel(self):
        print('level --destroy')
        self.level.world.level = None
        self.level.world = None
        self.level.units.level = None
        self.level.units = None
        self.level.middleLayer.level = None
        self.level.middleLayer = None
        del self.level



