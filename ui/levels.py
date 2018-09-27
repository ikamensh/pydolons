from PySide2 import QtCore


from ui.gameworld import GameWorld, MidleLayer
from content.dungeons.demo_dungeon import demo_dungeon
from ui.units import Units, BasicUnit
from ui.gui_util.GameProxyChanel import GameProxyChanel

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

class BaseLevel(object):
    def __init__(self):
        super(BaseLevel, self).__init__()
        self.gameRoot = None
        self.middleLayer = None
        self.world = None
        self.units = None

    def setGameRoot(self, gameRoot):
        self.gameRoot =  gameRoot
        self.gameRoot.currentLevel = self

    def setMiddleLayer(self, middleLayer):
        self.middleLayer = middleLayer
        self.middleLayer.level =  self

    def setGameWorld(self, world):
        self.world = world
        self.world.level = self

    def setUnits(self, units):
        self.units = units
        self.units.level = self

class Level_demo_dungeon(BaseLevel):

    def __init__(self, gameconfig):
        super(Level_demo_dungeon, self).__init__()
        self.gameconfig = gameconfig
        self.z_values = [ i for i in range(demo_dungeon.w)]
        self.gamechanel = GameProxyChanel()
        self.gamechanel.unitDied.connect(self.unitDiedSlot)
        self.gamechanel.unitMove.connect(self.unitMoveSlot)
        self.gamechanel.targetDamage.connect(self.targetDamageSlot)

    def unitDiedSlot(self, msg):
        print('died slot run')
        self.units.dieadUnit(msg.get('unit'))
        self.middleLayer.removeUnitLayer(msg.get('unit').uid)

    def unitMoveSlot(self, msg):
        print('move slot run')
        self.units.moveUnit(msg.get('unit'), msg.get('cell_to'))
        self.middleLayer.moveSupport(self.units.units_at[msg.get('unit').uid])

    def targetDamageSlot(self, msg):
        print('target Damage run')
        self.middleLayer.updateSupport(msg.get('target'), msg.get('amount'))

    def setUpLevel(self, game, controller):
        self.setGameWorld(GameWorld(self.gameconfig))
        self.world.setWorldSize(demo_dungeon.w, demo_dungeon.h)
        self.world.setFloor(self.gameconfig.getPicFile('floor.png'))

        self.setMiddleLayer(MidleLayer(self.gameconfig))
        self.game = game

        self.setUpUnits(self.game.battlefield)
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
            gameUnit.setWorldPos(unit_pos.x, unit_pos.y)
            gameUnit.uid = unit.uid
            self.units.addToGroup(gameUnit)
            # добавили gameunit
            self.units.units_at[unit.uid] = gameUnit

        self.units.active_unit = self.units.units_at[self.game.turns_manager.get_next().uid]
        self.units.setUnitStack(self.game.turns_manager.managed)
        self.middleLayer.createSuppot(self.units.units_at)
