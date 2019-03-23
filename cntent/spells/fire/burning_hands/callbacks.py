from __future__ import annotations
from mechanics.damage import Damage, DamageTypes
from mechanics.events import DamageEvent

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mechanics.actives import Active

def burning_hands_callback(active: Active, _):
    source = active.owner

    spell = active.spell
    n_damage = spell.amount

    bf = active.game.bf
    starting_location = source.cell
    facing = source.facing

    units_hit = bf.units_in_area(bf.cone(starting_location, facing, angle_max=spell.radius*20, dist_min=1, dist_max=spell.range))

    dmg = Damage(n_damage, DamageTypes.FIRE)

    for unit in units_hit:
        DamageEvent(dmg, target=unit, source=source)


