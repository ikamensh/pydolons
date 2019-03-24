from __future__ import annotations
from mechanics.AI import SearchNode
import copy
from battlefield import Cell
from game_objects.battlefield_objects import BattlefieldObject

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from battlefield import Battlefield
    from game_objects.battlefield_objects import Unit
    from typing import Tuple, Union, Set
    from mechanics.actives import Active
    from mechanics.factions import Faction

class SimGame:
    gamelog = None
    units: Set[Unit] = None
    bf: Battlefield = None


    def simulation(self):
        sim = copy.deepcopy(self)
        sim.is_sim = True
        sim.gamelog.mute()

        return sim


    def get_all_neighbouring_states(self, _unit: Unit):

        unit = self.find_unit(_unit)
        if unit is None:
            return []
        choices = self.get_all_choices(unit)
        nodes = [self.get_neighbour(c) for c in choices]
        return nodes

    def get_neighbour(self, c:Tuple[Active, Union[Cell, BattlefieldObject, None]]):

        active, target = c
        if active.simulate_callback:
            sim = None
        else:
            sim = self.step_into_sim(active, target)

        return SearchNode(SearchNode(None,None,self), c, sim)

    def step_into_sim(self, active: Active, target: Union[Cell, BattlefieldObject, None]):

        sim = self.simulation()
        sim_active = sim.find_active(active)
        sim_target = sim.find_unit(target) if isinstance(target, BattlefieldObject) else target
        sim_active.activate(sim_target)

        return sim


    def fake_measure(self, choice: Tuple[Active, Union[Cell, BattlefieldObject, None]],
                     fraction: Faction, use_position=True):
        active, target = choice
        with active.simulate(target):
            return self.utility(fraction, use_position=use_position)

    def delta(self, choice: Tuple[Active, Union[Cell, BattlefieldObject, None]], fraction = None):
        _fraction = fraction or choice[0].owner.faction
        _delta = self.get_neighbour(choice).utility(_fraction) - self.utility(_fraction)
        return _delta


    # The marvel of convoluted math,
    # we evaluate how good the game is for a given fraction with a single number!
    def utility(self, faction, use_position=True):
        total = 0

        own_units = [unit for unit in self.units if unit.faction is faction]
        opponent_units = [unit for unit in self.units if unit.faction is not faction]

        total += sum([self.unit_utility(unit) for unit in own_units])
        total -= sum([self.unit_utility(unit) for unit in opponent_units])

        if use_position:
            position_util = self.position_utility(own_units, opponent_units) / \
                            (1 + 1e13 * len(self.units))
            total += position_util

        return total

    def position_utility(self, own, opponent):

        total = 0
        for own_unit in own:
            for other in opponent:
                importance = (self.unit_utility(own_unit) * self.unit_utility(other)) ** (1/2)

                dist = self.bf.distance(own_unit, other)

                # the closer the better
                distance_util = 1e5 * (6 - dist **(1/2)) * importance
                assert distance_util >= 0
                total += distance_util

                # we want to face towards opponents
                if dist > 0:
                    own_facing_util = 1e9 * (1/dist) * \
                                      (6 - self.bf.angle_to(own_unit, other)[0] / 45) * importance
                    assert own_facing_util >= 0
                    total += own_facing_util

                    #its best for opponents to face away from us
                    opponent_facing_away_util = (1/dist) * self.bf.angle_to(other, own_unit)[0] \
                                                / 45 * importance
                    assert opponent_facing_away_util >= 0
                    total += opponent_facing_away_util

        # DELTA SPLIT!
        # for unit in own:
        #     for other in own:
        #         importance = (unit.utility * other.utility) ** (1 / 2)
        #         total -= importance * self.bf.distance(unit, other) ** (1/2)

        return total

    @staticmethod
    def unit_utility(unit: Unit):

        hp_factor = 1 + unit.health
        other_factors = 1
        # + (unit.mana + unit.stamina + unit.readiness*3) * len(unit.actives) / 1000
        magnitude = sum([unit.str, unit.end, unit.agi, unit.prc, unit.int, unit.cha])

        utility = magnitude * hp_factor * 1 * other_factors

        if hasattr(unit, "utility_factor"):
            utility *= unit.utility_factor

        return utility



    # extracting all possible transitions

    def get_all_choices(self, unit: Unit):
        actives = unit.actives

        choices = []
        for a in actives:
            if a.affordable():
                tgts = self.get_possible_targets(a)
                if tgts:
                    choices += [(a, tgt) for tgt in tgts]
                elif tgts is None:
                    choices.append( (a, None) )

        return choices


    def get_possible_targets(self, active):

        targeting_cls = active.targeting_cls
        if targeting_cls is None:
            return None

        result = list()

        if targeting_cls is Cell:
            for c in self.bf.all_cells:
                if active.check_target(c):
                    result.append(c)
            return result

        if targeting_cls is BattlefieldObject:
            for unit in self.bf.all_objs:
                if active.check_target(unit):
                    result.append(unit)
            return result

    # Identifying objects between different sim instances
    def find_unit(self, unit: Unit):
        return self.find_unit_by_uid(unit.uid)

    def find_active(self, active: Active):
        return self.find_active_by_uid(active.uid)

    def find_unit_by_uid(self, unit_uid: int) -> BattlefieldObject:
        for other in self.bf.all_objs:
            if unit_uid == other.uid:
                return other

    def find_active_by_uid(self, active_uid: int) -> Active:
        for unit in self.units:
            for other in unit.actives:
                if active_uid == other.uid:
                    return other


    @staticmethod
    def cost_heuristic(unit: Unit, factors = None):
        _factors = factors or {}

        def _(active):
            cost = active.cost
            hp_relative_cost = cost.health / unit.health * _factors.get("hp", 1)
            mana_relative_cost = cost.mana / unit.mana * _factors.get("mana", 0.5)
            stamina_relative_cost = cost.stamina / unit.stamina * _factors.get("stamina", 0.5)
            readiness_cost = cost.readiness * _factors.get("rdy", 0.1)

            return sum( (hp_relative_cost,
                         mana_relative_cost,
                         stamina_relative_cost,
                         readiness_cost) )

        return _