from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit

from mechanics.events import Trigger
from mechanics.events import MovementEvent, AttackEvent, DamageEvent
from mechanics.chances.CritHitGrazeMiss import ImpactFactor


def punish_move_attack_conditioned_cb(t: Trigger, e: MovementEvent):
    chance = t.zone_control_chance

    if e.game.random.random() < chance:
        unit = t.zone_control_unit
        actives_validity = {active: active.check_target(e.unit) and active.affordable() for active in unit.attack_actives}
        valid_actives = [k for k, v in actives_validity.items() if v is True]
        punishing_action = e.game.random.choice(valid_actives)

        spy = []
        e.game.events_platform.history.append( spy )
        punishing_action.activate(e.unit)

        attk_events = [event for event, happened in spy if isinstance(event, AttackEvent) and event.source is unit]
        for attk_event in attk_events:
            if attk_event.impact is not ImpactFactor.MISS:
                e.interrupted = True
                unit.pay(punishing_action.cost / 2)
                break

        e.game.events_platform.history.remove(spy)


def punish_move_damage_conditioned_cb(t: Trigger, e: MovementEvent):
    chance = t.zone_control_chance

    if e.game.random.random() < chance:
        unit = t.zone_control_unit
        actives_validity = {active: active.check_target(e.unit) and active.affordable() for active in unit.attack_actives}
        valid_actives = [k for k, v in actives_validity.items() if v is True]
        punishing_action = e.game.random.choice(valid_actives)

        spy = []
        e.game.events_platform.history.append( spy )
        punishing_action.activate(e.unit)

        dmg_events = [event for event, happened in spy if isinstance(event, DamageEvent) and event.source is unit]
        for dmg_event in dmg_events:
            if dmg_event.amount > 0:
                e.interrupted = True
                break

        e.game.events_platform.history.remove(spy)


def cond_enemy_moves(t, e: MovementEvent):
    return t.zone_control_unit.faction != e.unit.faction


def cond_from_within_radius(t, e: MovementEvent):
    initial_location = e.cell_from
    return e.game.bf.distance(t.zone_control_unit, initial_location) <= t.zone_control_radius


def cond_not_disabled(t, e):
    return not t.zone_control_unit.disabled

def cond_readiness_threshold(t, e):
    return t.zone_control_unit.readiness > 0


def cond_can_attack(t, e: MovementEvent):
    opportunities = [active.check_target(e.unit) and active.affordable() for active in t.zone_control_unit.attack_actives]
    return any(opportunities)


def zone_control_trigger(unit: Unit, radius, chance):


    trig = Trigger(MovementEvent,
                   platform = unit.game.events_platform,
                   is_interrupt = True,

                   conditions = {cond_enemy_moves,
                          cond_from_within_radius,
                          cond_not_disabled,
                          cond_readiness_threshold,
                          cond_can_attack},

                   callbacks = [punish_move_attack_conditioned_cb])

    trig.zone_control_unit = unit
    trig.zone_control_radius = radius
    trig.zone_control_chance = chance

    return trig


def zone_control_damage_cond_trigger(unit: Unit, radius, chance):


    trig = Trigger(MovementEvent,
                   platform = unit.game.events_platform,
                   is_interrupt = True,

                   conditions = {cond_enemy_moves,
                          cond_from_within_radius,
                          cond_not_disabled,
                          cond_readiness_threshold,
                          cond_can_attack},

                   callbacks = [punish_move_damage_conditioned_cb])

    trig.zone_control_unit = unit
    trig.zone_control_radius = radius
    trig.zone_control_chance = chance

    return trig
