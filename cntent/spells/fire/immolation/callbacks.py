from __future__ import annotations
from cntent.spells.fire.immolation.buffs import build_burning_buff
from mechanics.events import BuffAppliedEvent
from mechanics.damage import Damage, DamageTypes

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mechanics.actives import Active
    from game_objects.battlefield_objects import BattlefieldObject


def immolation_callback(active: Active, target: BattlefieldObject):
    source = active.owner
    spell = active.spell

    buff = build_burning_buff(dps=Damage(spell.amount, DamageTypes.FIRE),
                              source=source,
                              duration=spell.duration)

    BuffAppliedEvent(buff, target)
