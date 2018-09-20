from PySide2 import QtCore


from ui.gameworld import GameWorld, MidleLayer
from content.dungeons.demo_dungeon import demo_dungeon
from ui.units import Units, BasicUnit


class DemoGameTread(QtCore.QThread):

    finished = QtCore.Signal(str)

    def __init__(self, ):
        super(DemoGameTread, self).__init__()

    def setGame(self, game):
        self.game = game

    def createDemoDungeon(self):
        time = self.game.loop()
        return time

    def run(self):
        self.finished.emit(self.createDemoDungeon())



class Level_demo_dungeon:

    def __init__(self, gameconfig):
        self.gameconfig = gameconfig
        self.z_values = [ i for i in range(demo_dungeon.w)]

    def unitDied(self, unit):
        del self.units.units_at[unit]
        p = self.units.unit_locations[unit].x, self.units.unit_locations[unit].y
        del self.units.locations[p]
        del self.units.unit_locations[unit]


    def setUpLevel(self, game, controller):
        self.world = GameWorld(self.gameconfig)
        self.world.setWorldSize(demo_dungeon.w, demo_dungeon.h)
        self.world.setFloor(self.gameconfig.getPicFile('floor.png'))

        self.middleLayer = MidleLayer(self.gameconfig)
        self.middleLayer.setUpLevel(self)
        self.game = game

        self.setUpUnits(self.game.battlefield)
        self.gameconfig.setWorld(self.world)
        controller.setUp(self.world, self.units, self.middleLayer)


    def printResult(self, time):
        print('time = ',time)

    def setUpUnits(self, battlefield):
        self.units = Units()
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

            self.units.addToGroup(gameUnit)
            self.units.units_bf[unit.uid] = unit
            self.units.units_at[unit.uid] = gameUnit
            self.units.units_location[(gameUnit.worldPos.x(), gameUnit.worldPos.y())] = gameUnit
            self.units.locations.append(gameUnit.worldPos)

        self.units.active_unit = self.units.units_at[self.game.turns_manager.get_next().uid]
        self.units.setUnitStack(self.game.turns_manager.managed)
        self.middleLayer.createHPBar()



