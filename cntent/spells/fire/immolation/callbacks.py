from __future__ import annotations
from mechanics.damage import Damage, DamageTypes

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mechanics.actives import Active
    from game_objects.battlefield_objects import BattlefieldObject


from mechanics.events import BuffAppliedEvent
from cntent.spells.fire.immolation.buffs import build_burning_buff

def immolation_callback(active: Active, target:BattlefieldObject):
    source = active.owner
    spell = active.spell


    buff = build_burning_buff(dps=Damage(spell.amount, DamageTypes.FIRE),
                              source=source,
                              duration=spell.duration)

    BuffAppliedEvent(buff, target)