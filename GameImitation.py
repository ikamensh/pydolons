from battlefield.Battlefield import Battlefield, Cell
from mechanics.turns import AtbTurnsManager
from mechanics.fractions import Fractions
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
        unit_locations[hero] = dungeon.hero_entrance

        self.the_hero = hero

        self.fractions = {unit:Fractions.ENEMY for unit in unit_locations if not unit.is_obstacle}
        self.fractions[hero] = Fractions.PLAYER

        units_who_make_turns = [unit for unit in unit_locations.keys()
                                if not unit.is_obstacle]
        # self.turns_manager = AtbTurnsManager(self, units_who_make_turns)
        self.turns_manager = TurnsManager()
        self.turns_manager.unit = self.the_hero
        self.turns_manager.setUnits(unit_locations)

        self.add_many(unit_locations.keys(), unit_locations, self.fractions)


    def add_many(self, units, locations, fractions, facings = None):
        facings = facings or {unit: 1j for unit in units}
        for unit in units:
            if unit.is_obstacle:
                self.add_obstacle(unit, locations[unit])
            else:
                self.add_unit(unit, locations[unit], fractions[unit], facings.get(unit, 1j))

    def add_unit(self, unit, cell, fraction=Fractions.NEUTRALS, facing=None):
        unit.game = self
        for a in unit.actives:
            a.game = self
        self.fractions[unit] = fraction
        self.battlefield.place(unit, cell, facing)
        # self.turns_manager.add_unit(unit)
        unit.alive = True

    def unit_died(self, unit):
        self.battlefield.remove(unit)
        # self.turns_manager.remove_unit(unit)
        unit.alive = False

    def obstacle_destroyed(self, obstacle):
        self.battlefield.remove(obstacle)
        obstacle.alive = False

    def add_obstacle(self, obstacle, cell):
        self.battlefield.place(obstacle, cell)

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
