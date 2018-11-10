from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels, DamageEvent
from mechanics.chances.CritHitGrazeMiss import ImpactFactor
from typing import TYPE_CHECKING, Tuple
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit, BattlefieldObject
    from game_objects.items import Weapon
    from mechanics.chances.CritHitGrazeMiss import ImpactChances


class AttackEvent(Event):
    channel = EventsChannels.AttackChannel
    def __init__(self, source: Unit, target: BattlefieldObject, weapon : Weapon=None, fire: bool=True):
        game = source.game
        self.source = source
        self.target = target
        self.weapon = weapon or source.get_melee_weapon()
        self.is_backstab = not target.is_obstacle and not game.battlefield.x_sees_y(target, source)
        self.is_blind = not game.battlefield.x_sees_y(source, target)

        precision, evasion = self.effective_precision_evasion()
        self.impact = self.weapon.chances.actual(precision, evasion).roll_impact(random=game.random)

        super().__init__(game,fire)

    def check_conditions(self) -> bool:
        return all( (self.source, self.source.alive, self.target, self.target.alive, self.weapon, self.weapon.durability is None or self.weapon.durability > 0) )

    def resolve(self) -> None:

        if self.impact is not ImpactFactor.MISS:
            dmg_event = DamageEvent( self.weapon.damage, self.target, source=self.source, impact_factor = self.impact)

            if self.weapon and self.weapon.durability:
                self.weapon.durability -= dmg_event.weapon_dur_dmg
        else:
            self.game.gamelog("MISS")



    def calculate_chances(self) -> ImpactChances:
        p, e = self.effective_precision_evasion()
        return self.source.unarmed_chances.actual(p, e)


    def effective_precision_evasion(self)-> Tuple[float, float]:
        effective_precision = self.source.melee_precision
        if self.is_blind:
            effective_precision *= 0.25

        effective_evasion = self.target.melee_evasion
        if self.is_backstab:
            effective_evasion *= 0.25

        return effective_precision, effective_evasion


    def __repr__(self):
        msg = ""
        msg += "Backstab! " if self.is_backstab else ""
        msg += "Blind attack! " if self.is_blind else ""
        return msg + f"{self.source} attacks { self.target}."
