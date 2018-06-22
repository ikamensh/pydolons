from mechanics.abstract.event.Event import Event
from mechanics.abstract.effects.AttackEffect import AttackEffect
from mechanics.abstract.event.event_targeting.EventTargeting import EventTargeting

attack_unit_event = Event([AttackEffect], EventTargeting.TARGET_UNIT)
attack_cell_event = Event([AttackEffect], EventTargeting.UNIT_ON_TARGET_CELL)