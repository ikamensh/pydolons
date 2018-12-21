from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mechanics.actives import Active

from game_objects.battlefield_objects import Unit
from cntent.monsters.tel_razi import Golem

from mechanics.events import DamageEvent
from mechanics.damage import DamageTypes, Damage


def give_charges_callback(n):
    def _(active  :Active, target :Unit):
        if isinstance(target, Golem):
            target.golem_charge += n
            target.golem_charge = min(target.golem_charge, target.golem_max_charge)
        elif isinstance(target, Unit):
            dmg = Damage(10*n + target.mana * n / 20, DamageTypes.LIGHTNING)
            DamageEvent(dmg, target, source=active.owner)
    return _

