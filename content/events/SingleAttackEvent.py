from mechanics.flexi_targeting.event.Event import Event
from content.effects.AttackEffect import AttackEffect
from mechanics.flexi_targeting.event.event_targeting.EventTargeting import EventTargeting

attack_unit_event = Event([AttackEffect], EventTargeting.TARGET_UNIT)
attack_cell_event = Event([AttackEffect], EventTargeting.UNIT_ON_TARGET_CELL)