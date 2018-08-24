from gameworld import GameWorld, MidleLayer
#
from DreamGame import DreamGame
from content.base_types.demo_hero import demohero_basetype
from content.dungeons.demo_dungeon import demo_dungeon
from game_objects.battlefield_objects import Unit
from mechanics.events import MovementEvent
#
from units import *
#
from PySide2.QtCore import Slot

class DemoGameTread(QtCore.QThread):
    """docstring for DemoGameTread."""
    finished = QtCore.Signal(str)
    # unitMove = QtCore.Signal(str)
    def __init__(self, ):
        super(DemoGameTread, self).__init__()

    def setGame(self, game):
        self.game = game

    def createDemoDungeon(self):
        #
        # game = DreamGame.start_dungeon(demo_dungeon, Unit(demohero_basetype))
        time = self.game.loop()
        #
        return time

    def run(self):
        self.finished.emit(self.createDemoDungeon())
        # self.unitMove.emit()





class Level_demo_dungeon(object):
    """docstring for Level_demo_dungeon."""
    def __init__(self, gameconfig):
        super(Level_demo_dungeon, self).__init__()
        self.gameconfig = gameconfig
        self.z_values = [ i for i in range(demo_dungeon.w)]

    def setController(self, controller):
        self.controller = controller

    def unitDied(self, unit):
        del self.units.units_at[unit]
        p = self.units.unit_locations[unit].x, self.units.unit_locations[unit].y
        del self.units.locations[p]
        del self.units.unit_locations[unit]


    def setUpLevel(self, game ):
        # setUP world
        self.world = GameWorld(self.gameconfig)
        self.world.setWorldSize(demo_dungeon.w, demo_dungeon.h)
        self.world.setFloor(self.gameconfig.getPicFile('floor.png'))
        # setUp midle
        self.midleLayer = MidleLayer(self.gameconfig)
        self.midleLayer.setUpLevel(self)
        # setUp game manager
        self.game = game
        # setUp units
        self.setUpUnits(self.game.battlefield)
        # setUp curent game configuration
        self.gameconfig.setUpLevel(self.world)
        # setUp curent game configuration for controller
        self.controller.setUp(self.world, self.units, self.midleLayer)


    def printResult(self, time):
        print('time = ',time)

    def setUpUnits(self, battlefield):
        self.units = Units()
        # setUp units
        self.units.unit_locations = {}
        self.units.locations = []

        for unit, unit_pos in battlefield.unit_locations.items():
            gameUnit = BasicUnit(self.gameconfig.unit_size[0], self.gameconfig.unit_size[1], gameconfig = self.gameconfig)
            if unit.icon == 'hero.png':
                self.active_unit = True
            gameUnit.setPixmap(self.gameconfig.getPicFile(unit.icon))
            gameUnit.setWorldPos(unit_pos.x - 4, unit_pos.y -4)
            print('uid = ',unit.uid)
            gameUnit.uid = unit.uid
            # gameUnit.setBefore(unit_pos.x*1.1)
            self.units.addToGroup(gameUnit)
            self.units.units_bf[unit.uid] = unit
            self.units.units_at[unit.uid] = gameUnit
            self.units.units_location[(gameUnit.worldPos.x(), gameUnit.worldPos.y())] = gameUnit
            self.units.locations.append(gameUnit.worldPos)
            # self.units.activateNextUnit()
        self.units.active_unit = self.units.units_at[self.game.active_unit.uid]
        self.units.setUnitStack(self.game.turns_manager.managed)
        self.midleLayer.createHPBar()
        # add hero
        # self.hero = BasicUnit(self.res.unit_width, self.res.unit_height)
        # self.hero.setPixmap(self.res.hero)
        # self.hero.setWorldPos(demo_dungeon.hero_entrance.x - 4, demo_dungeon.hero_entrance.y - 4)
        # self.units.addToGroup(self.hero)
        # self.units.hero = self.hero

    # @Slot()
    # def timerSlot(self):
    #     # print('helo')
    #     for unit, unit_pos in self.game.battlefield.unit_locations.items():
    #         # print('uid = ',unit.uid)
    #         # print('self.units = ',self.units)
    #         gameUnit = self.units.units_at[unit.uid]
    #         gameUnit.setWorldPos(unit_pos.x - 4, unit_pos.y - 4)
    #         # print(gameUnit.worldPos)
    #         # self.units.unit_locations.update((unit, unit_pos))
