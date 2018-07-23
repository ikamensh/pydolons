from mechanics.turns import TurnsManager
from GameLog import gamelog
from my_utils.utils import flatten
from game_objects.battlefield_objects import Unit
from mechanics.buffs import Buff

import random

epsilon = 1e-6
class AtbTurnsManager(TurnsManager):
    def __init__(self, units=None):
        self.managed = []
        if units:
            for unit in units:
                self.add_unit(unit)

            buffs = list(flatten([unit.buffs for unit in units]))
            self.managed += buffs
        self.time = 0
        gamelog(f"Action turn based battle started. its {self.time} now")


    def pass_time(self, time):
        for m in list(self.managed):
            if isinstance(m, Unit):
                m.readiness += m.initiative * time / 10
            elif isinstance(m, Buff):
                m.duration -= time

        self.time += time
        gamelog(f"{time} seconds passes. its {self.time} now")

    @staticmethod
    def time_until_turn(managee):
        if isinstance(managee, Unit):

            if managee.disabled:
                return 1e300

            readiness_missing = 1 - managee.readiness
            if readiness_missing <= 0:
                return 0
            time_unitl_next_turn = readiness_missing * 10 / managee.initiative + epsilon
            return time_unitl_next_turn

        elif isinstance(managee, Buff):
            return managee.duration

    def get_next(self):

        self.sort()
        next_managed = self.managed[0]
        while not isinstance(next_managed, Unit):
            self.pass_time(self.time_until_turn(next_managed))
            self.sort()
            next_managed = self.managed[0]

        if next_managed.readiness >= 1:
            assert 1.1 >= next_managed.readiness >= 1
            return next_managed
        else:
            self.pass_time(self.time_until_turn(next_managed))

            new_closest_unit = self.managed[0]
            assert 1.1 >= new_closest_unit.readiness >= 1
            return new_closest_unit

    def sort(self):
        self.managed.sort(key=self.time_until_turn)


    def add_unit(self, unit):
        if unit not in self.managed:
            self.managed.append(unit)
            unit.readiness = random.random() * 0.25

    def remove_unit(self, unit):
        assert unit in self.managed
        self.managed.remove(unit)

    def add_buff(self, buff):
        self.managed.append(buff)

    def remove_buff(self, buff):
        self.managed.remove(buff)


