from __future__ import annotations

from battlefield.Battlefield import Battlefield, Cell
from mechanics.turns import AtbTurnsManager
from mechanics.fractions import Fractions
from mechanics.AI import BruteAI, RandomAI
from mechanics.events import EventsPlatform, NextUnitEvent
from ui.events import LevelStatusEvent
from mechanics.rpg.experience import exp_rule
from mechanics.rpg.regen import regen_rule
from exceptions import PydolonsException, CantAffordActiveException
from multiplayer.events.ServerOrderIssuedEvent import ServerOrderIssuedEvent
from multiplayer.events.ClientOrderIssuedEvent import ClientOrderIssuedEvent
from GameLog import GameLog, LogTargets

import copy
import time
import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict
    from game_objects.battlefield_objects import Unit, Obstacle


class DreamGame:

    def __init__(self, bf=None, rules=None, is_sim = False, is_server=True, seed = None):
        self.random = random.Random(seed) if seed else random.Random(100)
        self.battlefield : Battlefield = bf or Battlefield(8,8)
        self.the_hero : Unit= None
        self.fractions : Dict[Unit,Fractions] = {}
        self.enemy_ai = BruteAI(self)
        self.random_ai = RandomAI(self)
        self.gamelog = GameLog(LogTargets.PRINT)
        self.events_platform = EventsPlatform(self.gamelog)
        self.turns_manager = AtbTurnsManager(self)
        self.is_sim = is_sim
        self.loop_state = True
        self.player_turn_lock = False
        self.is_server = is_server

        for rule in (rules or [exp_rule, regen_rule]):
            rule(self)

    @classmethod
    def start_dungeon(cls, dungeon, hero: Unit, is_server=True):

        bf = Battlefield(dungeon.h, dungeon.w)
        game = cls(bf, is_server=is_server)


        unit_locations = dungeon.unit_locations(game)
        unit_locations[hero] = dungeon.hero_entrance

        game.the_hero = hero

        fractions = {unit:Fractions.ENEMY for unit in unit_locations if not unit.is_obstacle}
        fractions[hero] = Fractions.PLAYER

        units_who_make_turns = [unit for unit in unit_locations.keys()
                                if not unit.is_obstacle]
        game.turns_manager = AtbTurnsManager(game, units_who_make_turns)

        game.add_many(unit_locations.keys(), unit_locations, fractions)


        return game

    def add_many(self, units, locations, fractions, facings = None):
        facings = facings or {unit: 1j for unit in units}
        for unit in units:
            if unit.is_obstacle:
                self.add_obstacle(unit, locations[unit])
            else:
                self.add_unit(unit, locations[unit], fractions[unit], facings.get(unit, 1j))



    def add_unit(self, unit: Unit, cell,  fraction=Fractions.NEUTRALS, facing = None):
        unit.game = self
        for a in unit.actives:
            a.game = self
        self.fractions[unit] = fraction
        self.battlefield.place(unit, cell, facing)
        self.turns_manager.add_unit(unit)
        unit.alive = True


    def unit_died(self, unit: Unit):
        self.battlefield.remove(unit)
        self.turns_manager.remove_unit(unit)
        unit.alive = False


    def obstacle_destroyed(self, obstacle: Obstacle):
        self.battlefield.remove(obstacle)
        obstacle.alive = False


    def add_obstacle(self, obstacle, cell):
        self.battlefield.place(obstacle, cell)


    def loop(self):
        while self.loop_state:
            game_over = self.game_over()
            if game_over:
                print(game_over)
                return self.turns_manager.time


            active_unit = self.turns_manager.get_next()
            if self.fractions[active_unit] == Fractions.PLAYER:
                self.player_turn_lock = True
                # don't stop game loop
                while self.player_turn_lock and self.loop_state :
                    time.sleep(0.02)
                continue
            else:
                NextUnitEvent(active_unit)
                try:
                    active, target = self.enemy_ai.decide_step(active_unit)
                except:
                    active, target = self.random_ai.decide_step(active_unit)
                self.order_action(active_unit, active, target)



    def game_over(self):
        own_units = [unit for unit in self.fractions if self.fractions[unit] is Fractions.PLAYER and unit.alive]
        enemy_units = [unit for unit in self.fractions if self.fractions[unit] is Fractions.ENEMY and unit.alive]

        if len(own_units) == 0:
            LevelStatusEvent(self, "DEFEAT")
            return "DEFEAT"
        elif len(enemy_units) == 0:
            LevelStatusEvent(self, "VICTORY")
            return "VICTORY"
        else:
            return None


    def __repr__(self):
        return f"{'Simulated ' if self.is_sim else ''}{self.battlefield.h} by {self.battlefield.w} dungeon with {len(self.battlefield.units_at)} units in it."

    def order_step(self, c_vec):
        if self.turns_manager.get_next() is self.the_hero:
            cell_from = self.battlefield.unit_locations[self.the_hero]
            facing = self.battlefield.unit_facings[self.the_hero]
            cell_to = Cell.from_complex( cell_from.complex + c_vec * facing )
            self.ui_order(cell_to.x, cell_to.y)

    def ui_order(self, x, y):
        print(f"ordered: move to {x},{y}")

        if self.turns_manager.get_next() is self.the_hero:
            cell = Cell.from_complex(x + y* 1j)
            if cell in self.battlefield.units_at:
                self.order_attack(self.the_hero, random.choice(self.battlefield.units_at[cell]))
            else:
                self.order_move(self.the_hero, cell)


    def order_turn_cw(self):
        if self.turns_manager.get_next() is self.the_hero:
            self._order_turn(ccw=False)

    def order_turn_ccw(self):
        if self.turns_manager.get_next() is self.the_hero:
            self._order_turn(ccw=True)


    def _order_turn(self, ccw):
        active = self.the_hero.turn_ccw_active if ccw else self.the_hero.turn_cw_active
        self.order_action(self.the_hero, active, None)

    @staticmethod
    def _complain_missing(unit, actives, action):
        if unit.stamina < min([a.cost.stamina for a in actives]):
            missing = "stamina"
        elif unit.mana < min([a.cost.mana for a in actives]):
            missing = "mana"
        # elif unit.health < min([a.cost.health for a in actives]):
        else:
            missing = "health"

        raise CantAffordActiveException(action, missing)

    def order_move(self, unit: Unit, target_cell: Cell, AI_assist=True):


        if not 0 <= target_cell.x < self.battlefield.w or not 0 <= target_cell.y < self.battlefield.h:
            raise PydolonsException("Can't move there!")

        cell_from = self.battlefield.unit_locations[unit]
        if cell_from == target_cell:
            raise PydolonsException("Unit is already at the target cell.")

        actives = unit.movement_actives
        if len(actives) == 0:
            if unit is self.the_hero:
                raise PydolonsException("The hero is immobilized.")


        affordable_actives = [a for a in actives if a.owner_can_afford_activation()]

        if not affordable_actives:
            self._complain_missing(unit, actives, "move")

        valid_actives = [a for a in affordable_actives if a.check_target(target_cell)]

        if valid_actives:
            chosen_active = min(valid_actives, key=DreamGame.cost_heuristic(unit))
            self.order_action(unit, chosen_active, target_cell)
            return
        else:
            # We can't directly execute this order.
            if not AI_assist:
                raise PydolonsException("None of the user movement actives can reach the target cell.")
            else:
                facing = self.battlefield.unit_facings[unit]
                angle, ccw = Cell.angle_between(facing, target_cell.complex - cell_from.complex)
                if angle > 45:
                    active = unit.turn_ccw_active if ccw else unit.turn_cw_active
                    self.order_action(unit, active, None)
                    return

                distance = self.battlefield.distance(unit, target_cell)

                if distance >= 2:
                    vec = target_cell.complex - cell_from.complex
                    vec_magnitude_1 = vec / abs(vec)
                    closer_target = Cell.from_complex(cell_from.complex + vec_magnitude_1)
                    self.order_move(unit, closer_target)
                else:
                    raise PydolonsException("None of the user movement actives can reach the target.")


    def order_attack(self, unit: Unit, _target: Unit, AI_assist=True):
        actives = unit.attack_actives
        if len(actives) == 0:
            raise PydolonsException("The unit has no attack actives.")

        if isinstance(_target, Cell):
            units = self.get_units_at(_target)
            if units is None:
                raise PydolonsException("Can't attack an empty cell.")
            unit_target = random.choice(units)
        else:
            unit_target = _target

        affordable_actives = [a for a in actives if a.owner_can_afford_activation()]

        if not affordable_actives:
            self._complain_missing(unit, actives, "attack")

        valid_actives = [a for a in affordable_actives if a.check_target(unit_target)]

        if valid_actives:
            chosen_active = min(valid_actives, key=DreamGame.cost_heuristic(unit))
            self.order_action(unit, chosen_active, unit_target)
            return
        else:
            if not AI_assist:
                raise PydolonsException("None of the user attack actives can reach the target.")
            else:
                target_cell = self.battlefield.unit_locations[unit_target]
                cell_from = self.battlefield.unit_locations[unit]

                facing = self.battlefield.unit_facings[unit]
                angle, ccw = Cell.angle_between(facing, target_cell.complex -cell_from.complex)
                if angle > 45:
                    active = unit.turn_ccw_active if ccw else unit.turn_cw_active
                    self.order_action(unit, active, None)
                    return

                distance = self.battlefield.distance(unit, target_cell)
                if distance >= 2:
                    self.order_move(unit, target_cell)
                else:
                    raise PydolonsException("None of the user attack actives can reach the target.")


    def order_action(self, unit, active, target):
        if target is None:
            _target = None
        elif isinstance(target, Cell):
            _target = target
        else:
            _target = target.uid

        if self.is_server:
            assert self.turns_manager.get_next() is unit
            ServerOrderIssuedEvent(self, unit.uid, active.uid, _target)
            unit.activate(active, target)
            self.player_turn_lock = False
        else:
            ClientOrderIssuedEvent(self, unit.uid, active.uid, _target)


    @staticmethod
    def cost_heuristic(unit: Unit, factors = None):
        _factors = factors or {}

        def _(active):
            cost = active.cost
            hp_relative_cost = cost.health / unit.health * _factors.get("hp", 1)
            mana_relative_cost = cost.mana / unit.mana * _factors.get("mana", 0.5)
            stamina_relative_cost = cost.stamina / unit.stamina * _factors.get("stamina", 0.5)
            readiness_cost = cost.readiness * _factors.get("rdy", 0.1)

            return sum( (hp_relative_cost, mana_relative_cost, stamina_relative_cost, readiness_cost) )

        return _



    @property
    def units(self):
        return [unit for unit in self.battlefield.unit_locations if not unit.is_obstacle]

    def get_location(self, unit: Unit):
        return self.battlefield.unit_locations[unit]


    def get_units_at(self, coord):
        return self.battlefield.get_units_at(coord)


    def get_units_distances_from(self, p):
        return self.battlefield.get_units_dists_to(p)


    def print_all_units(self):
        for unit, cell in self.battlefield.unit_locations.items():
            x, y = cell.x, cell.y
            print(f"There is a {unit} at ({x},{y})")
