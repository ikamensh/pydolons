from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from mechanics.damage import Damage, DamageTypes
import mechanics.events as events
from mechanics.chances import roll
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit

class PushEvent(Event):
    channel = EventsChannels.PushChannel

    def __init__(self, unit: Unit, push_against: Unit):
        game = unit.game
        self.bf = game.bf
        self.unit = unit
        self.push_against = push_against
        self.cell_to = push_against.cell


        super().__init__(game)

    def check_conditions(self):
        return self.unit.alive

    def resolve(self):

        dmg_factor = 0.05
        damage = Damage( (self.unit.max_health + self.push_against.max_health)* dmg_factor, type=DamageTypes.CRUSH)
        events.DamageEvent(damage, self.push_against, source=self.unit)
        events.DamageEvent(damage, self.unit, source=self.push_against)

        if self.unit.alive and self.push_against.alive:
            pushed_to = self.game.random.choice(self.bf.get_cells_within_dist(self.cell_to, 1))
            success = roll(0.6, self.unit.str * 2, self.push_against.str * 2, self.game.random)

            if success:
                victor, loser = self.unit, self.push_against
            else:
                victor, loser = self.push_against, self.unit

            events.MovementEvent(loser, pushed_to)

            pusher_atb_cost = 0.4
            pushed_atb_cost = 0.7
            loser.readiness -= pushed_atb_cost
            victor.readiness -= pusher_atb_cost



    def __repr__(self):
        return f"{self.unit} pushes against {self.push_against} to {self.cell_to}"




