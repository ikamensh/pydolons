from mechanics.events import EventsChannels
from mechanics.events.src.Event import Event
from mechanics.damage import Damage
from mechanics.chances import ImpactFactor

class DamageEvent(Event):
    channel = EventsChannels.DamageChannel

    def __init__(self, damage, target, *, source=None, impact_factor=ImpactFactor.HIT):
        self.source = source
        self.target = target
        self.damage = damage
        self.impact_factor = impact_factor

        self.weapon_dur_dmg = None

        super().__init__()


    @property
    def amount(self):
        return Damage.calculate_damage(self.damage, self.target, self.impact_factor)[0]


    def check_conditions(self):
        return self.target.alive and self.amount > 0

    def resolve(self):
        _ , armor_dur_dmg, weapon_dur_dmg = Damage.calculate_damage(self.damage, self.target, self.impact_factor)

        if not self.target.is_obstacle:
            body_armor = self.target.equipment["body"]
            if body_armor and body_armor.durability:
                body_armor.durability -= armor_dur_dmg

        self.weapon_dur_dmg = weapon_dur_dmg
        self.target.lose_health(self.amount, self.source)



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
