from game_objects.battlefield_objects import BattlefieldObject
from mechanics.AI import SearchNode
from battlefield.Battlefield import Cell
from GameLog import gamelog
from DreamGame import DreamGame
from contextlib import contextmanager
import my_context
import copy

class SimGame(DreamGame):

    @contextmanager
    def temp_context(self):
        old_game = my_context.the_game
        my_context.the_game = self
        yield
        my_context.the_game = old_game

    @contextmanager
    def simulation(self):
        sim = copy.deepcopy(self)
        sim.is_sim = True
        with gamelog.muted(), sim.temp_context():
            yield sim


    def get_all_neighbouring_states(self, _unit):

        with self.temp_context():
            unit = self.find_unit(_unit)
            if unit is None:
                return []
            choices = self.get_all_choices(unit)
            nodes = [self.get_neighbour(c) for c in choices]
            return nodes

    def get_neighbour(self, c):

        active, target = c
        if active.simulate_callback:
            sim = None
        else:
            sim = self.step_into_sim(active, target)

        return SearchNode(SearchNode(None,None,self), c, sim)

    def step_into_sim(self, active, target):

        with self.simulation() as sim:
            sim_active = sim.find_active(active)
            sim_target = sim.find_unit(target) if isinstance(target, BattlefieldObject) else target
            sim_active.activate(sim_target)

        return sim


    def fake_measure(self, choice, fraction, use_position=True):
        active, target = choice
        with self.temp_context():
            with active.simulate(target):
                return self.utility(fraction, use_position=use_position)

    def delta(self, choice, fraction = None):
        _fraction = fraction or self.fractions[choice[0].owner]
        _delta = self.get_neighbour(choice).utility(_fraction) - self.utility(_fraction)
        return _delta


    # The marvel of convoluted math,
    # we evaluate how good the game is for a given fraction with a single number!
    def utility(self, fraction, use_position=True):
        total = 0

        own_units = [unit for unit in self.units if self.fractions[unit] is fraction]
        opponent_units = [unit for unit in self.units if self.fractions[unit] is not fraction]

        total += sum([self.unit_utility(unit) for unit in own_units])
        total -= sum([self.unit_utility(unit) for unit in opponent_units])

        if use_position:
            position_util = self.position_utility(own_units, opponent_units) / (1 + 1e13 * len(self.units))
            total += position_util

        return total

    def position_utility(self, own, opponent):

        total = 0
        for own_unit in own:
            for other in opponent:
                importance = (self.unit_utility(own_unit) * self.unit_utility(other)) ** (1/2)

                dist = self.battlefield.distance(own_unit, other)

                # the closer the better
                distance_util = 1e5 * (6 - dist **(1/2)) * importance
                assert distance_util >= 0
                total += distance_util

                # we want to face towards opponents
                own_facing_util = 1e9 * (1/dist) * ( 6 - self.battlefield.angle_to(own_unit, other)[0] / 45) * importance
                assert own_facing_util >= 0
                total += own_facing_util

                #its best for opponents to face away from us
                opponent_facing_away_util = (1/dist) * self.battlefield.angle_to(other, own_unit)[0] / 45 * importance
                assert opponent_facing_away_util >= 0
                total += opponent_facing_away_util

        # DELTA SPLIT!
        # for unit in own:
        #     for other in own:
        #         importance = (unit.utility * other.utility) ** (1 / 2)
        #         total -= importance * self.battlefield.distance(unit, other) ** (1/2)

        return total

    @staticmethod
    def unit_utility(unit):
        hp_factor = 1 + unit.health
        other_factors = 1 # + (unit.mana + unit.stamina + unit.readiness*3) * len(unit.actives) / 1000
        magnitude = sum([unit.str, unit.end, unit.agi, unit.prc, unit.int, unit.cha])
        return magnitude * hp_factor * 1 * other_factors



    # extracting all possible transitions

    def get_all_choices(self, unit):
        actives = unit.actives

        choices = []
        for a in actives:
            if a.owner_can_afford_activation():
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
            for c in self.battlefield.all_cells:
                if active.check_target(c):
                    result.append(c)
            return result

        if targeting_cls is BattlefieldObject:
            for unit in self.battlefield.unit_locations:
                if active.check_target(unit):
                    result.append(unit)
            return result



    # Identifying objects between different sim instances

    def find_unit(self, unit):
        for other in self.battlefield.unit_locations:
            if unit.uid == other.uid:
                return other

    def find_active(self, active):
        for unit in self.battlefield.unit_locations:
            for other in unit.actives:
                if active.uid == other.uid:
                    return other

    def find_unit_by_uid(self, unit_uid):
        for other in self.battlefield.unit_locations:
            if unit_uid == other.uid:
                return other

    def find_active_by_uid(self, active_uid):
        for unit in self.battlefield.unit_locations:
            for other in unit.actives:
                if active_uid == other.uid:
                    return other