from __future__ import annotations

from battlefield import Battlefield, Cell, Facing, Vision
from mechanics.turns import AtbTurnsManager
from mechanics.factions import Faction
from mechanics.AI import BruteAI, RandomAI
from mechanics.events import EventsPlatform, NextUnitEvent
from ui.events import LevelStatusEvent
from mechanics.rpg.experience import exp_rule
from mechanics.rpg.regen import regen_rule
from mechanics.rpg.push import push_rule
from mechanics.rpg.aggro import vision_aggro_rule, damage_provokes_rule

from exceptions import PydolonsError, CantAffordActiveError
from multiplayer.events.ServerOrderIssuedEvent import ServerOrderIssuedEvent
from multiplayer.events.ClientOrderIssuedEvent import ClientOrderIssuedEvent
from GameLog import GameLog, LogTargets
from mechanics.AI.SimGame import SimGame

import time
import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Dict, List, Union
    from game_objects.battlefield_objects import Unit, Obstacle
    from game_objects.dungeon.Dungeon import Dungeon


class DreamGame(SimGame):
    default_rules = [exp_rule,
                     regen_rule,
                     push_rule,
                     vision_aggro_rule,
                     damage_provokes_rule]

    def __init__(self, bf=None, rules=None, is_sim = False, is_server=True, seed = None):

        self.is_sim = is_sim
        self.is_server = is_server
        self.random = random.Random(seed) if seed else random.Random(100)
        self.units = set()
        self.obstacles = set()
        self.bf : Battlefield = bf or Battlefield(8, 8)
        self.bf.game = self
        self.vision = Vision(self)

        self.the_hero : Unit= None

        self.enemy_ai = BruteAI(self)
        self.random_ai = RandomAI(self)
        self.wondering_ai = RandomAI(self, chance_pass=0.66)

        self.gamelog = GameLog(LogTargets.PRINT)
        self.events_platform = EventsPlatform(self.gamelog)
        self.turns_manager = AtbTurnsManager(self)

        self.loop_state = True
        self.player_turn_lock = False


        for rule in (rules or DreamGame.default_rules):
            rule(self)

    @classmethod
    def start_dungeon(cls, dungeon: Dungeon, hero: Unit, is_server=True):

        bf = Battlefield(dungeon.h, dungeon.w)
        game = cls(bf, is_server=is_server)
        bf.game = game


        game.the_hero = hero
        hero.cell = dungeon.hero_entrance
        hero.faction = Faction.PLAYER

        objs = dungeon.objs(game)
        for o in objs:
            if o.is_obstacle:
                game.add_obstacle(o)
            else:
                game.add_unit(o)

        units_who_make_turns = [unit for unit in objs if not unit.is_obstacle]
        game.turns_manager = AtbTurnsManager(game, units_who_make_turns)

        return game

    def add_unit(self, unit: Unit, cell = None, faction = None, facing = None):
        if cell is not None: unit.cell = cell
        if faction is not None: unit.faction = faction
        if facing is not None: unit.facing = facing

        assert unit.cell
        assert unit.facing
        assert unit.faction

        unit.game = self
        for a in unit.actives:
            a.game = self

        unit.fights_hero = False

        self.turns_manager.add_unit(unit)
        self.units.add(unit)
        unit.update()


    def unit_died(self, unit: Unit):
        unit.alive = False
        self.turns_manager.remove_unit(unit)
        self.units.remove(unit)
        unit.deactivate_abilities()



    def obstacle_destroyed(self, obstacle: Obstacle):
        obstacle.alive = False
        self.obstacles.remove(obstacle)


    def add_obstacle(self, obstacle: Obstacle, cell = None):
        obstacle.game = self
        self.obstacles.add(obstacle)
        if cell:
            obstacle.cell = cell

    def loop(self, turns = None):
        n_turns = 0
        player_in_game = not bool(self.game_over())

        while self.loop_state:
            n_turns += 1
            if turns and n_turns > turns:
                break

            if player_in_game:
                game_over = self.game_over()
                if game_over:
                    print(game_over)
                    return self.turns_manager.time


            active_unit = self.turns_manager.get_next()
            if active_unit.faction == Faction.PLAYER:
                self.player_turn_lock = True

                while self.player_turn_lock and self.loop_state :
                    time.sleep(0.02)
                continue

            else:
                NextUnitEvent(active_unit)

                ai = self.enemy_ai if active_unit.fights_hero else self.wondering_ai
                active, target = ai.decide_step(active_unit)

                if active:
                    self.order_action(active_unit, active, target)
                else:
                    active_unit.readiness -= 0.5



    def game_over(self):

        if len(self.player_units) == 0:
            LevelStatusEvent(self, "DEFEAT")
            return "DEFEAT"
        elif len(self.enemy_units) == 0:
            LevelStatusEvent(self, "VICTORY")
            return "VICTORY"
        else:
            return None


    def __repr__(self):
        return f"{'Simulated ' if self.is_sim else ''}{self.bf.h} by" \
            f" {self.bf.w} dungeon with {len(self.units)} units in it."

    def order_step(self, c_vec):
        if self.turns_manager.get_next() is self.the_hero:
            cell_from = self.the_hero.cell
            facing = self.the_hero.facing
            cell_to = Cell.from_complex( cell_from.complex + c_vec * facing )
            self.ui_order(cell_to.x, cell_to.y)

    def ui_order(self, x, y):
        print(f"ordered: move to {x},{y}")

        if self.turns_manager.get_next() is self.the_hero:
            cell = Cell.from_complex(x + y* 1j)
            if cell in self.bf.cells_to_units:
                self.order_attack(self.the_hero, random.choice(self.bf.cells_to_units[cell]))
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

        raise CantAffordActiveError(action, missing)

    # refactor?
    def order_move(self, unit: Unit, target_cell: Cell, AI_assist=True):

        target_cell = Cell.maybe_complex(target_cell)

        if not 0 <= target_cell.x < self.bf.w or not 0 <= target_cell.y < self.bf.h:
            raise PydolonsError("Can't move there!")

        cell_from = unit.cell
        if cell_from == target_cell:
            raise PydolonsError("Unit is already at the target cell.")

        actives = unit.movement_actives
        if len(actives) == 0:
            if unit is self.the_hero:
                raise PydolonsError("The hero is immobilized.")


        affordable_actives = [a for a in actives if a.affordable()]

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
                raise PydolonsError("None of the user movement actives can reach "
                                        "the target cell.")

            angle, ccw = Cell.angle_between(unit.facing,
                                            target_cell.complex - cell_from.complex)
            if angle > 45:
                active = unit.turn_ccw_active if ccw else unit.turn_cw_active
                self.order_action(unit, active, None)
                return

            distance = self.bf.distance(unit, target_cell)

            if distance >= 2:
                vec = target_cell.complex - cell_from.complex
                vec_magnitude_1 = vec / abs(vec)
                closer_target = Cell.from_complex(cell_from.complex + vec_magnitude_1)
                self.order_move(unit, closer_target)
            else:
                raise PydolonsError("None of the user movement actives can reach the target.")


    def order_attack(self, unit: Unit, _target: Unit, AI_assist=True):
        actives = unit.attack_actives
        if len(actives) == 0:
            raise PydolonsError("The unit has no attack actives.")

        if isinstance(_target, Cell):
            units = self.get_units_at(_target)
            if units is None:
                raise PydolonsError("Can't attack an empty cell.")
            unit_target = random.choice(units)
        else:
            unit_target = _target

        affordable_actives = [a for a in actives if a.affordable()]

        if not affordable_actives:
            self._complain_missing(unit, actives, "attack")

        valid_actives = [a for a in affordable_actives if a.check_target(unit_target)]

        if valid_actives:
            chosen_active = min(valid_actives, key=DreamGame.cost_heuristic(unit))
            self.order_action(unit, chosen_active, unit_target)
            return
        else:
            if not AI_assist:
                raise PydolonsError("None of the user attack actives can reach the target.")
            else:
                target_cell = unit_target.cell

                angle, ccw = Cell.angle_between(unit.facing, target_cell.complex -unit.cell.complex)
                if angle > 45:
                    active = unit.turn_ccw_active if ccw else unit.turn_cw_active
                    self.order_action(unit, active, None)
                    return

                distance = self.bf.distance(unit, target_cell)
                if distance >= 2:
                    self.order_move(unit, target_cell)
                else:
                    raise PydolonsError("None of the user attack actives can reach the target.")


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
    def enemy_units(self) -> List[Unit]:
        return [u for u in self.units if u.faction is Faction.ENEMY]

    @property
    def player_units(self) -> List[Unit]:
        return [u for u in self.units if u.faction is Faction.PLAYER]

    def get_units_at(self, coord: Union[Cell, complex]):
        coord = Cell.maybe_complex(coord)
        return [u for u in self.units if u.cell == coord]

    def get_units_distances_from(self, p):
        return self.bf.get_units_dists_to(p, self.units)


    def print_all_units(self):
        for unit in self.units:
            print(f"There is a {unit} at ({unit.cell.x},{unit.cell.y})")
