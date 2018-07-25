from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels, DamageEvent
from mechanics.chances.CritHitGrazeMiss import ImpactCalculator, ImpactFactor
from GameLog import gamelog

import my_context


class AttackEvent(Event):
    channel = EventsChannels.AttackChannel
    def __init__(self, source, target, weapon=None):
        self.source = source
        self.target = target
        self.weapon = weapon or source.get_melee_weapon()
        self.is_backstab = not target.is_obstacle and not my_context.the_game.battlefield.x_sees_y(target, source)
        self.is_blind = not my_context.the_game.battlefield.x_sees_y(source, target)
        super().__init__()

    def check_conditions(self):
        return all( (self.source, self.source.alive, self.target, self.target.alive, self.weapon, self.weapon.durability is None or self.weapon.durability > 0) )

    def resolve(self):

        effective_precision = self.source.melee_precision
        if self.is_blind:
            effective_precision *= 0.25

        effective_evasion = self.target.melee_evasion
        if self.is_backstab:
            effective_evasion *= 0.25

        impact = ImpactCalculator.roll_impact(self.source.unarmed_chances,
                                              effective_precision,
                                              effective_evasion)
        if impact is not ImpactFactor.MISS:
            unit_died = DamageEvent(None, self.target, weapon=self.weapon, source=self.source, impact_factor = impact)
            self.result = unit_died
        else:
            gamelog("MISS")

    def __repr__(self):
        msg = ""
        msg += "Backstab! " if self.is_backstab else ""
        msg += "Blind attack! " if self.is_blind else ""
        return msg + f"{self.source} attacks { self.target}."