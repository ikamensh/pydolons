from battlefield.Battlefield import Battlefield, Cell
from mechanics.turns import AtbTurnsManager
from mechanics.factions import Faction
import time
import random


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict
    from game_objects.battlefield_objects import Unit, Obstacle

class TurnsManager:
    def __init__(self):
        self.unit = None
        self.unit_locations = None
        self.managed_units = None

    def setUnits(self, units):
        self.unit_locations = units
        self.managed_units = list(units.keys())


    def get_next(self):
        return self.unit

    def managed_units(self):
        return list(self.unit_locations.values())

class GameLog:
    def __init__(self):
        self.msg = 'game imitation'

class DreamGame:

    def __init__(self, dungeon, hero, is_server=True):
        seed = 5
        self.gamelog = GameLog()
        self.random = random.Random(seed) if seed else random.Random(100)
        self.loop_state = True
        self.battlefield = Battlefield(dungeon.h, dungeon.w)
        print(hero)
        print(dungeon.unit_locations)
        unit_locations = dungeon.unit_locations(self)
        print('debug')
        hero.cell = dungeon.hero_entrance

        self.the_hero = hero

        self.faction = {unit:Faction.ENEMY for unit in unit_locations if not unit.is_obstacle}
        self.faction[hero] = Faction.PLAYER

        units_who_make_turns = [unit for unit in unit_locations.keys()
                                if not unit.is_obstacle]
        # self.turns_manager = AtbTurnsManager(self, units_who_make_turns)
        self.turns_manager = TurnsManager()
        self.turns_manager.unit = self.the_hero
        self.turns_manager.setUnits(unit_locations)

        self.add_many(unit_locations.keys(), unit_locations, self.faction)

    def add_unit(self, unit, cell, fraction=Faction.NEUTRALS, facing=None):
        unit.game = self
        for a in unit.actives:
            a.game = self
        self.faction[unit] = fraction
        self.bf.place(unit, cell, facing)
        # self.turns_manager.add_unit(unit)
        unit.alive = True

    def unit_died(self, unit):
        self.bf.remove(unit)
        # self.turns_manager.remove_unit(unit)
        unit.alive = False

    def obstacle_destroyed(self, obstacle):
        self.bf.remove(obstacle)
        obstacle.alive = False

    def add_obstacle(self, obstacle, cell):
        self.bf.place(obstacle, cell)

    def ui_order(self, *args, **kwargs):
        self.gamelog.msg = 'ui_order'

    def order_step(self, *args, **kwargs):
        self.gamelog.msg = 'order_step'

    def order_turn_ccw(self):
        self.gamelog.msg = 'order_turn_ccw'

    def order_turn_cw(self):
        self.gamelog.msg = 'order_turn_cw'




    def loop(self, turns=None):
        while self.loop_state:
            time.sleep(0.2)
        print('stop game loop')
