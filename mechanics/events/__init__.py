from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mechanics.events.combat.DamageEvent import DamageEvent
    from mechanics.events.combat.AttackEvent import AttackEvent
    from mechanics.events.combat.RangedAttackEvent import RangedAttackEvent

from mechanics.events.src.EventChannels import EventsChannels

from mechanics.events.src.Event import Event
from mechanics.events.src.Trigger import Trigger
from mechanics.events.src.Interrupt import CounteredInterrupt, PermanentInterrupt, Trigger

from mechanics.events.TimePassedEvent import TimePassedEvent
from mechanics.events.combat.PushEvent import PushEvent
from mechanics.events.combat.MovementEvent import MovementEvent
from mechanics.events.TurnEvent import TurnEvent
from mechanics.events.NextUnitEvent import NextUnitEvent


from mechanics.events.combat.HealingEvent import HealingEvent
from mechanics.events.ActiveEvent import ActiveEvent

from mechanics.events.combat.ObstacleDestroyedEvent import ObstacleDestroyedEvent
from mechanics.events.items.ItemUsedUpEvent import ItemUsedUpEvent
from mechanics.events.items.ItemDroppedEvent import ItemDroppedEvent
from mechanics.events.items.ItemDestroyedEvent import ItemDestroyedEvent
from mechanics.events.combat.UnitDiedEvent import UnitDiedEvent

from mechanics.events.magic.BuffAppliedEvent import BuffAppliedEvent
from mechanics.events.magic.BuffDetachedEvent import BuffDetachedEvent
from mechanics.events.magic.BuffExpiredEvent import BuffExpiredEvent
from mechanics.events.magic.BuffDispelledEvent import BuffDispelledEvent

from mechanics.events.src.EventsPlatform import EventsPlatform

importers = {}
def damage_event():
    global DamageEvent
    from mechanics.events.combat.DamageEvent import DamageEvent as de
    DamageEvent = de
    return de

importers['DamageEvent'] = damage_event

def attack_event():
    global AttackEvent
    from mechanics.events.combat.AttackEvent import AttackEvent as ae
    AttackEvent = ae
    return ae

importers['AttackEvent'] = attack_event

def ranged_attack_event():
    global RangedAttackEvent
    from mechanics.events.combat.RangedAttackEvent import RangedAttackEvent as ae
    RangedAttackEvent = ae
    return ae

importers['RangedAttackEvent'] = ranged_attack_event

def __getattr__(name):
    if name in importers:
        return importers[name]()
