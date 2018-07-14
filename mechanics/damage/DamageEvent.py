from mechanics.events.EventsPlatform import EventsChannels
from mechanics.events.Event import Event
from mechanics.events import UnitDiedEvent
from mechanics.damage import Damage
from mechanics.chances import ImpactFactor

class DamageEvent(Event):
    channel = EventsChannels.DamageChannel

    def __init__(self, damage, target, *,  source=None, impact_factor=ImpactFactor.HIT):
        self.source = source
        self.target = target
        self.damage = damage
        self.impact_factor = impact_factor
        self.result = False
        super().__init__()


    @property
    def amount(self):
        return Damage.calculate_damage(self.damage, self.target, self.impact_factor)

    def check_conditions(self):
        return self.target.alive and self.amount > 0

    def resolve(self):
        unit_0_hp = self.target.lose_health(self.amount)
        if unit_0_hp:
            UnitDiedEvent(self.target, self.source)



    def __repr__(self):

        if self.amount == 0:
            return "{}! {} laughs at the attempts to damage it with {}"\
                .format(self.impact_factor, self.target, self.damage.type)

        if self.source:
            return "{}! {} recieves {} {} damage from {}.".format(
                                                                self.impact_factor,
                                                                self.target,
                                                                self.amount,
                                                                self.damage.type,
                                                                self.source)
        else:
            return "{}! {} recieves {} {} damage.".format(self.impact_factor,
                                                          self.target,
                                                          self.amount,
                                                          self.damage.type)