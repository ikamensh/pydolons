from __future__ import annotations
from mechanics.events import EventsChannels
from mechanics.events.src.Event import Event
from mechanics.chances import ImpactFactor
from mechanics.damage import Damage
from game_objects.items import EquipmentSlotUids

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import BattlefieldObject, Unit


class DamageEvent(Event):
    channel = EventsChannels.DamageChannel

    def __init__(
            self,
            damage: Damage,
            target: BattlefieldObject,
            *,
            source: Unit = None,
            impact_factor=ImpactFactor.HIT,
            fire=True):
        self.source = source
        self.target = target
        self.damage = damage
        self.impact_factor = impact_factor

        self.weapon_dur_dmg = 0

        super().__init__(target.game, fire, logging=True)

    @property
    def amount(self):
        return Damage.calculate_damage(
            self.damage, self.target, self.impact_factor)[0]

    def check_conditions(self):
        return self.target.alive

    def resolve(self):

        _, armor_dur_dmg, weapon_dur_dmg = Damage.calculate_damage(
            self.damage, self.target, self.impact_factor)

        if not self.target.is_obstacle:
            body_armor = self.target.equipment[EquipmentSlotUids.BODY]
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
