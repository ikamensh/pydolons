from __future__ import annotations
from cntent.actives.std.buffs.std_buffs import rest_buff, onguard_buff
from mechanics.events import BuffAppliedEvent
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mechanics.actives import Active


def onguard_callback(active: Active, target: None):
    BuffAppliedEvent(onguard_buff(), active.owner)


def rest_callback(active: Active, target: None):
    active.owner.mana += active.owner.max_mana / 20
    active.owner.stamina += active.owner.max_stamina / 10

    BuffAppliedEvent(rest_buff(), active.owner)
