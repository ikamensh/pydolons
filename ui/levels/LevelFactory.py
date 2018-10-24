from ui.GameWorld import GameWorld
from ui.units import UnitMiddleLayer
from cntent.dungeons.demo_dungeon import demo_dungeon
from ui.units import Units, BasicUnit
from game_objects import battlefield_objects as bf_objs

from ui.levels.BaseLevel import BaseLevel


class LevelFactory:
    def __init__(self, logicEngine):
        self.LEngine = logicEngine
        pass

    def getLevel(self, name):
        # level = None
        self.buildLevel(name)
        return self.level


    def buildLevel(self, name):
        self.level = BaseLevel()
        self.z_values = [i for i in range(self.level.w)]
        self.setUpLevel(self.LEngine.game)


    def removeLevel(self):
        pass

    def sevaLevelState(self):
        pass

    def setUpLevel(self, game):
        self.level.setGameWorld(GameWorld(self.gameRoot.cfg))
        self.level.world.setWorldSize(demo_dungeon.w, demo_dungeon.h)
        self.level.world.setFloor(self.gameRoot.cfg.getPicFile('floor.png'))

        self.level.setMiddleLayer(UnitMiddleLayer(self.gameRoot.cfg))
        self.level.game = game

        self.level.setUpUnits(self.level.game.battlefield)
        self.level.gameRoot.cfg.setWorld(self.level.world)
        self.level.gameRoot.controller.setUp(self.level.world, self.level.units, self.level.middleLayer)

    def setUpUnits(self, battlefield):
        self.level.setUnits(Units())
        for unit, unit_pos in battlefield.unit_locations.items():
            gameUnit = BasicUnit(self.gameRoot.cfg.unit_size[0], self.gameRoot.cfg.unit_size[1], gameconfig=self.gameRoot.cfg)
            if unit.icon == 'hero.png':
                self.active_unit = True
            gameUnit.setPixmap(self.gameRoot.cfg.getPicFile(unit.icon))
            if isinstance(unit, bf_objs.Unit):
                gameUnit.setDirection(battlefield.unit_facings[unit])
            gameUnit.setWorldPos(unit_pos.x, unit_pos.y)
            gameUnit.uid = unit.uid
            self.level.units.addToGroup(gameUnit)
            # добавили gameunit
            self.level.units.units_at[unit.uid] = gameUnit

        self.level.units.active_unit = self.level.units.units_at[self.level.game.turns_manager.get_next().uid]
        self.level.middleLayer.createSuppot(self.level.units.units_at)

