from __future__ import annotations
from mechanics.events import HealingEvent
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mechanics.actives import Active


def healing_potion_cb(amount):
    def _(active: Active, target: None):
        HealingEvent(amount, active.owner)
    return _


def mana_potion_cb(amount):
    def _(active: Active, target: None):
        active.owner.mana += amount
    return _


def stamina_potion_cb(amount):
    def _(active: Active, target: None):
        active.owner.stamina += amount
    return _
