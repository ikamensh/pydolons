from __future__ import annotations
from my_utils.utils import flatten

from game_objects.battlefield_objects import Unit

from mechanics.turns import TurnsManager
from mechanics.buffs import Buff
from mechanics.events import TimePassedEvent
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from DreamGame import DreamGame

epsilon = 1e-6
class AtbTurnsManager(TurnsManager):
    def __init__(self, game: DreamGame):
        self.game = game
        self.managed = []
        if game.units:
            for unit in game.units:
                self.add_unit(unit)

            buffs = list(flatten([unit.buffs for unit in game.units]))
            self.managed += buffs
        self.time = 0
        game.gamelog(f"Action turn based battle started. its {self.time} now")

    @property
    def managed_units(self):
        return [elem for elem in self.managed if isinstance(elem, Unit)]

    def pass_time(self, time):

        for m in list(self.managed):
            if isinstance(m, Unit):
                m.readiness += m.initiative * time / 10
            elif isinstance(m, Buff):
                m.duration -= time

        self.time += time
        TimePassedEvent(self.game, time)
        # gamelog(f"{time:.3f} seconds passes. its {self.time:.3f} now")

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

    def get_next(self) -> Unit:
        self.sort()
        next_managed = self.managed[0]
        while not isinstance(next_managed, Unit):
            self.pass_time(self.time_until_turn(next_managed))
            self.sort()
            next_managed = self.managed[0]

        if next_managed.readiness >= 1:
            # assert 1.1 >= next_managed.readiness
            return next_managed
        else:
            self.pass_time(self.time_until_turn(next_managed))

            new_closest_unit = self.managed[0]
            # assert 1.1 >= new_closest_unit.readiness >= 1
            return new_closest_unit

    def sort(self):
        self.managed.sort(key=self.time_until_turn)


    def add_unit(self, unit):
        if unit not in self.managed:
            self.managed.append(unit)
            unit.readiness = self.game.random.random() * 0.25

    def remove_unit(self, unit):
        assert unit in self.managed
        self.managed.remove(unit)

    def add_buff(self, buff):
        self.managed.append(buff)

    def remove_buff(self, buff):
        self.managed.remove(buff)
