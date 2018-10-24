from ui.GameWorld import GameWorld
from ui.units import UnitMiddleLayer
from cntent.dungeons.demo_dungeon import demo_dungeon
from ui.units import Units, BasicUnit
from game_objects import battlefield_objects as bf_objs

from ui.levels.BaseLevel import BaseLevel



class Level_demo_dungeon(BaseLevel):

    def __init__(self, gameconfig):
        super(Level_demo_dungeon, self).__init__()
        self.gameconfig = gameconfig
        self.z_values = [ i for i in range(demo_dungeon.w)]

    def setUpLevel(self, game, controller):
        self.setGameWorld(GameWorld(self.gameconfig))
        self.world.setWorldSize(demo_dungeon.w, demo_dungeon.h)
        self.world.setFloor(self.gameconfig.getPicFile('floor.png'))

        self.setMiddleLayer(UnitMiddleLayer(self.gameconfig))
        self.game = game

        self.setUpUnits(self.game.battlefield)
        self.units.middleLayer = self.middleLayer
        self.gameconfig.setWorld(self.world)
        controller.setUp(self.world, self.units, self.middleLayer)

    def printResult(self, time):
        print('time = ',time)

    def setUpUnits(self, battlefield):
        self.setUnits(Units())

        for unit, unit_pos in battlefield.unit_locations.items():
            gameUnit = BasicUnit(self.gameconfig.unit_size[0], self.gameconfig.unit_size[1], gameconfig = self.gameconfig)
            if unit.icon == 'hero.png':
                self.active_unit = True
            gameUnit.setPixmap(self.gameconfig.getPicFile(unit.icon))
            if isinstance(unit, bf_objs.Unit):
                gameUnit.setDirection(battlefield.unit_facings[unit])
            gameUnit.setWorldPos(unit_pos.x, unit_pos.y)
            gameUnit.uid = unit.uid
            self.units.addToGroup(gameUnit)
            # добавили gameunit
            self.units.units_at[unit.uid] = gameUnit

        self.units.active_unit = self.units.units_at[self.game.turns_manager.get_next().uid]
        self.middleLayer.createSuppot(self.units.units_at)
