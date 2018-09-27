from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels, DamageEvent
from mechanics.chances.CritHitGrazeMiss import ImpactCalculator, ImpactFactor
from GameLog import gamelog
from ui.gui_util.gamechanel import gamechanel

import my_context


class AttackEvent(Event):
    channel = EventsChannels.AttackChannel
    def __init__(self, source, target, weapon=None, fire=True):
        self.source = source
        self.target = target
        self.weapon = weapon or source.get_melee_weapon()
        self.is_backstab = not target.is_obstacle and not my_context.the_game.battlefield.x_sees_y(target, source)
        self.is_blind = not my_context.the_game.battlefield.x_sees_y(source, target)
        super().__init__(fire)

    def check_conditions(self):
        return all( (self.source, self.source.alive, self.target, self.target.alive, self.weapon, self.weapon.durability is None or self.weapon.durability > 0) )

    def resolve(self):

        precision, evasion = self.effective_precision_evasion()

        #TODO replace with weapon chances as soon as available
        impact = ImpactCalculator.roll_impact(self.source.unarmed_chances, precision, evasion)
        if impact is not ImpactFactor.MISS:
            dmg_event = DamageEvent(self.weapon.damage, self.target, source=self.source, impact_factor = impact)

            if self.weapon and self.weapon.durability:
                self.weapon.durability -= dmg_event.weapon_dur_dmg
        else:
            gamelog("MISS")
            gamechanel.sendMessage({'event':'AttackEvent','msg':'MISS' })



    def calculate_chances(self):
        p, e = self.effective_precision_evasion()
        return ImpactCalculator.calc_chances(self.source.unarmed_chances, p, e)


    def effective_precision_evasion(self):
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
