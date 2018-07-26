from battlefield.Battlefield import Battlefield, Cell
from mechanics.turns import AtbTurnsManager
from mechanics.fractions import Fractions
from mechanics.AI import BruteAI, RandomAI, AstarAI
from mechanics.AI.SimGame import SimGame
from mechanics.events import EventsPlatform
import copy
import my_context

class DreamGame(SimGame):

    def __init__(self, bf, is_sim = False):
        self.battlefield = bf
        self.the_hero = None
        self.fractions = {}
        self.brute_ai = BruteAI(self)
        self.random_ai = RandomAI(self)
        self.turns_manager = AtbTurnsManager()
        self.events_platform = EventsPlatform()
        self.is_sim = is_sim

    @staticmethod
    def start_dungeon(dungeon, hero):

        unit_locations = dungeon.unit_locations
        unit_locations = copy.deepcopy(unit_locations)
        unit_locations[hero] = dungeon.hero_entrance
        bf = Battlefield(dungeon.h, dungeon.w)
        game = DreamGame(bf)
        if unit_locations:
            bf.place_many(unit_locations)
        game.the_hero = hero

        game.fractions.update({unit:Fractions.ENEMY for unit in unit_locations if not unit.is_obstacle})
        game.fractions[hero] = Fractions.PLAYER

        units_who_make_turns = [unit for unit in unit_locations.keys()
                                if not unit.is_obstacle]
        game.turns_manager = AtbTurnsManager(units_who_make_turns)
        game.set_to_context()

        return game



    def add_unit(self, unit, cell,  fraction):
        self.fractions[unit] = fraction
        self.battlefield.place(unit, cell)
        self.turns_manager.add_unit(unit)


    def unit_died(self, unit):
        del self.fractions[unit]
        self.battlefield.remove(unit)
        self.turns_manager.remove_unit(unit)
        unit.alive = False


    def obstacle_destroyed(self, obstacle):
        self.battlefield.remove(obstacle)


    def add_obstacle(self, obstacle, cell):
        self.battlefield.place(obstacle, cell)


    def loop(self):
        while True:
            active_unit = self.turns_manager.get_next()
            active, target = self.brute_ai.decide_step(active_unit)
            active_unit.activate(active, target)
            game_over = self.game_over()
            if game_over:
                print(game_over)
                return self.turns_manager.time


    def game_over(self):
        own_units = [unit for unit in self.fractions if self.fractions[unit] is Fractions.PLAYER]
        enemy_units = [unit for unit in self.fractions if self.fractions[unit] is Fractions.ENEMY]

        if len(own_units) == 0:
            return "DEFEAT"
        elif len(enemy_units) == 0:
            return "VICTORY"
        else:
            return None


    def __repr__(self):
        return f"{'Simulated ' if self.is_sim else ''}{self.battlefield.h} by {self.battlefield.w} dungeon with {len(self.battlefield.units_at)} units in it."


    def order_move(self, unit, target_cell, AI_assist=True):

        cell_from = self.battlefield.unit_locations[unit]
        if cell_from == target_cell:
            return False, "Unit is already at the target cell."

        actives = unit.movement_actives
        if len(actives) == 0:
            return False, "The unit has no movement actives."


        valid_actives = [a for a in actives if a.check_target(target_cell) and a.owner_can_afford_activation()]

        if len(valid_actives) == 0:
            # We can't directly execute this order.
            if AI_assist:
                facing = self.battlefield.unit_facings[unit]
                angle, ccw = Cell.angle_between(facing, target_cell.complex - cell_from.complex)
                if angle >= 45:
                    unit.turn_ccw() if ccw else unit.turn_cw()
                    return True, unit.turn_ccw_active if ccw else unit.turn_cw_active

                distance = self.battlefield.distance(unit, target_cell)

                if distance >= 2:
                    vec = target_cell.complex - cell_from.complex
                    vec_magnitude_1 = vec / abs(vec)
                    closer_target = Cell.from_complex(cell_from.complex + vec_magnitude_1)
                    return self.order_move(unit, closer_target)

            return False, "None of the user movement actives can reach the target cell."

        chosen_active = min(valid_actives, key=DreamGame.cost_heuristic(unit))
        chosen_active.activate(target_cell)

        return True, chosen_active


    def order_attack(self, unit, _target, AI_assist=True):
        unit_target = _target
        actives = unit.attack_actives
        if len(actives) == 0:
            return False, "The unit has no attack actives."

        if isinstance(unit_target, Cell):
            unit_target = self.battlefield.units_at.get(unit_target, None)
            if unit_target is None:
                return False, "Can't attack an empty cell."

        valid_actives = [a for a in actives if a.check_target(unit_target) and a.owner_can_afford_activation()]

        if len(valid_actives) == 0:
            if AI_assist:

                facing = self.battlefield.unit_facings[unit]
                target_cell = self.battlefield.unit_locations[unit_target]
                cell_from = self.battlefield.unit_locations[unit]
                angle, ccw = Cell.angle_between(facing, target_cell.complex -cell_from.complex)
                if angle >= 45:
                    unit.turn_ccw() if ccw else unit.turn_cw()
                    return True, unit.turn_ccw_active if ccw else unit.turn_cw_active

                distance = self.battlefield.distance(unit, target_cell)
                if distance >= 2:
                    return self.order_move(unit, target_cell)

            return False, "None of the user attack actives can reach the target."

        chosen_active = min(valid_actives, key=DreamGame.cost_heuristic(unit))
        chosen_active.activate(unit_target)

        return True, chosen_active


    @staticmethod
    def cost_heuristic(unit, factors = None):
        _factors = factors or {}

        def _(active):
            cost = active.cost
            hp_relative_cost = cost.health / unit.health * _factors.get("hp", 1)
            mana_relative_cost = cost.mana / unit.mana * _factors.get("mana", 0.5)
            stamina_relative_cost = cost.stamina / unit.stamina * _factors.get("stamina", 0.5)
            readiness_cost = cost.readiness * _factors.get("rdy", 0.1)

            return sum( (hp_relative_cost, mana_relative_cost, stamina_relative_cost, readiness_cost) )

        return _


    def set_to_context(self):
        my_context.the_game = self


    @property
    def units(self):
        return [unit for unit in self.battlefield.unit_locations if not unit.is_obstacle]

    def get_location(self, unit):
        assert unit in my_context.the_game.battlefield.unit_locations
        return self.battlefield.unit_locations[unit]


    def get_unit_at(self, coord):
        return self.battlefield.units_at[coord]


    def get_units_distances_from(self, p):
        return self.battlefield.get_units_dists_to(p)


    def print_all_units(self):
        for unit, cell in self.battlefield.unit_locations.items():
            x, y = cell.x, cell.y
            print(f"There is a {unit} at ({x},{y})")









