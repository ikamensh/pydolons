from mechanics.events.Event import Event
from mechanics.events.EventsPlatform import EventsChannels
from mechanics.damage import DamageEvent
from mechanics.chances.CritHitGrazeMiss import ImpactCalculator, ImpactFactor


class AttackEvent(Event):
    channel = EventsChannels.AttackChannel
    def __init__(self, source, target, weapon):
        self.source = source
        self.target = target
        self.weapon = weapon
        source.readiness -= 0.5
        super().__init__()

    def check_conditions(self):
        return all( (self.source, self.source.alive, self.target, self.target.alive, self.weapon, self.weapon.durability is None or self.weapon.durability > 0) )

    def resolve(self):
        self.source.readiness -= 0.5
        impact = ImpactCalculator.roll_impact(self.source.unarmed_chances, self.source.melee_precision,
                                              self.target.melee_evasion)
        if impact is not ImpactFactor.MISS:
            unit_died = DamageEvent(None, self.target, weapon=self.weapon, source=self.source, impact_factor = impact)
            self.result = unit_died
        else:
            print("MISS")

    def __repr__(self):
        return "{} attacks {}.".format(self.source, self.target)