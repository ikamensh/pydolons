from game_objects.battlefield_objects import BattlefieldObject
from mechanics.AI import SearchNode
from battlefield.Battlefield import Cell
from GameLog import gamelog
from contextlib import contextmanager
import my_context
import copy

class SimGame:


    @contextmanager
    def temp_context(self):
        old_game = my_context.the_game
        my_context.the_game = self
        yield
        my_context.the_game = old_game

    @contextmanager
    def simulation(self):
        old_game = my_context.the_game
        sim = copy.deepcopy(self)
        sim.is_sim = True
        my_context.the_game = sim
        with gamelog.muted():
            yield sim
        my_context.the_game = old_game

    def utility(self, fraction, schadenfreude = 5, use_position=True):
        total = 0

        own_units = [unit for unit in self.units if self.fractions[unit] is fraction]
        opponent_units = [unit for unit in self.units if self.fractions[unit] is not fraction]

        total += sum([unit.utility for unit in own_units])
        total -= sum([unit.utility for unit in opponent_units]) * schadenfreude

        if use_position:
            total += self.position_utility(own_units, opponent_units) / (1 + 100 * len(self.units))

        return total

    def position_utility(self, own, opponent, schadenfreude = 5):

        total = 0
        for own_unit in own:
            for other in opponent:
                importance = (own_unit.utility * other.utility) ** (1/2)

                dist = self.battlefield.distance(own_unit, other)

                # the closer the better
                total += (3 - dist **(1/2)) * schadenfreude * importance

                # we want to face towards opponents
                total += (1/dist) * ( 4 - self.battlefield.angle_to(own_unit, other)[0] / 45) * importance

                #its best for opponents to face away from us
                total += (1/dist) * self.battlefield.angle_to(other, own_unit)[0] / 45 * schadenfreude * importance

        for unit in own:
            for other in own:
                importance = (unit.utility * other.utility) ** (1 / 2)
                total -= importance * self.battlefield.distance(unit, other) ** (1/2)

        return total

    def delta_util(self, active, target, use_positions=True, schadenfreude = 5):

        fraction = self.fractions[active.owner]
        util_before = self.utility(fraction, schadenfreude, use_position=use_positions)

        if active.simulate_callback:
            return self.fake_measure((active, target), fraction, use_position=use_positions) - util_before

        with self.simulation() as sim:
            sim_action = sim.find_active(active)
            sim_target = sim.find_unit(target) if isinstance(target, BattlefieldObject) else target
            sim_action.activate(sim_target)
            util_after = sim.utility(fraction, schadenfreude, use_position=use_positions)

        return util_after - util_before

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

    def fake_measure(self, choice, fraction, use_position=True):

        active, target = choice
        with self.temp_context():
            with active.simulate(target):
                return self.utility(fraction, use_position=use_position)

    def get_all_neighbouring_states(self, _unit):
        with self.temp_context():
            unit = self.find_unit(_unit)
            choices = self.get_all_choices(unit)
            nodes = []
            for c in choices:
                active, target = c
                if active.simulate_callback:
                    sim = None
                else:
                    sim = self.step_into_sim(active, target)

                nodes.append( SearchNode(self, c, sim, self.fractions[unit]) )

            return nodes

    def step_into_sim(self, active, target):

        with self.simulation() as sim:
            sim_active = sim.find_active(active)
            sim_target = sim.find_unit(target) if isinstance(target, BattlefieldObject) else target
            sim_active.activate(sim_target)

        return sim

    def find_unit(self, unit):
        for other in self.battlefield.unit_locations:
            if unit.uid == other.uid:
                return other

    def find_active(self, active):
        for unit in self.battlefield.unit_locations:
            for other in unit.actives:
                if active.uid == other.uid:
                    return other