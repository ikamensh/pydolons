from PySide2 import QtCore

from ui.GameWorld import GameWorld
from ui.units import UnitMiddleLayer
from content.dungeons.demo_dungeon import demo_dungeon
from ui.units import Units, BasicUnit
from ui.gui_util.GameProxyChanel import GameProxyChanel

from ui.levels.BaseLevel import BaseLevel

import my_context


class Level_demo_dungeon(BaseLevel):

    def __init__(self, gameconfig):
        super(Level_demo_dungeon, self).__init__()
        self.gameconfig = gameconfig
        self.z_values = [ i for i in range(demo_dungeon.w)]
        self.gamechanel = GameProxyChanel()
        self.gamechanel.unitActive.connect(self.unitActiveSlot)
        self.gamechanel.unitDied.connect(self.unitDiedSlot)
        # self.gamechanel.unitMove.connect(self.unitMoveSlot)
        self.gamechanel.unitTurn.connect(self.unitTurnSlot)
        # self.gamechanel.targetDamage.connect(self.targetDamageSlot)
        # self.gamechanel.attackTo.connect(self.attackToSlot)

    def unitActiveSlot(self, msg):
        pass
        # print()
        # print(self.game.active_unit)
        # print(msg)

    def unitDiedSlot(self, msg):
        # print(msg)
        self.middleLayer.removeUnitLayer(msg.get('unit').uid)
        self.units.dieadUnit(msg.get('unit'))

    def unitMoveSlot(self, msg):
        self.gameRoot.cfg.sound_maps[msg.get('unit').sound_map.move].play()
        self.units.moveUnit(msg.get('unit'), msg.get('cell_to'))
        self.middleLayer.moveSupport(self.units.units_at[msg.get('unit').uid])

    def unitTurnSlot(self, msg):
        self.units.turnUnit(msg.get('uid'), msg.get('turn'))
        # print(msg)

    def targetDamageSlot(self, msg):
        # Требуется рефакторинг метод срабатывает после смерти юнита
        if msg.get('target').uid in self.units.units_at.keys():
            self.middleLayer.updateSupport(msg.get('target'), msg.get('amount'))
            self.gameRoot.cfg.sound_maps[msg.get('damage_type')].play()
            # print('debug -> damage_type', msg.get('damage_type'))
        pass

    def targetDamageHitSlot(self, msg):
        self.gameRoot.cfg.sound_maps[msg.get('sound')].play()

    def attackSlot(self, msg):
        # self.gameRoot.gamePages.gameMenu.showNotify(msg.get('msg'))
        self.gameRoot.cfg.sound_maps[msg.get('sound')].play()


    def setUpLevel(self, game, controller):
        self.setGameWorld(GameWorld(self.gameconfig))
        self.world.setWorldSize(demo_dungeon.w, demo_dungeon.h)
        self.world.setFloor(self.gameconfig.getPicFile('floor.png'))

        self.setMiddleLayer(UnitMiddleLayer(self.gameconfig))
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
            gameUnit.setDirection(battlefield.unit_facings[unit])
            gameUnit.setWorldPos(unit_pos.x, unit_pos.y)
            gameUnit.uid = unit.uid
            self.units.addToGroup(gameUnit)
            # добавили gameunit
            self.units.units_at[unit.uid] = gameUnit

        self.units.active_unit = self.units.units_at[self.game.turns_manager.get_next().uid]
        self.units.setUnitStack(self.game.turns_manager.managed)
        self.middleLayer.createSuppot(self.units.units_at)
