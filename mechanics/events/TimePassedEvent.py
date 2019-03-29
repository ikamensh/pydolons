from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from DreamGame import DreamGame


class TimePassedEvent(Event):
    channel = EventsChannels.TimePassedChannel

    def __init__(self, game: DreamGame, dt: float):
        self.time = game.turns_manager.time
        self.dt = dt
        super().__init__(game)

    def check_conditions(self):
        return True

    def resolve(self):
        # cooldowns expire
        for unit in list(self.game.units):
            if not unit.is_obstacle and unit.alive:
                for active in unit.actives:
                    active.remaining_cd = max(0, active.remaining_cd - self.dt)

    def __repr__(self):
        return f"{self.dt} time has passed."
