

from mechanics.damage import DamageEvent, Damage, DamageTypes
from content.spells import runes
from game_objects.spells import  SpellConcept, Spell
from character_creation.MasteriesEnum import MasteriesEnum
from mechanics.actives import SingleUnitTargeting, Costs, Active


def lightning_bolt_callback(active, single_unit_targeting):
    source = active.owner
    target = single_unit_targeting.target

    spell = active.spell
    n_damage = spell.amount
    dmg = Damage(n_damage, DamageTypes.LIGHTNING)

    DamageEvent(dmg, target=target, source=source)

concept = SpellConcept(name="lightning bolt",
                       school=MasteriesEnum.LIGHTNING,
                       targeting_cls=SingleUnitTargeting,
                       complexity=30,
                       costs=Costs(4, 40, 0, readiness_cost=1),
                       amount=60, duration=None, precision_factor=1,
                       distance=5, radius=None,
                       resolve_callback=lightning_bolt_callback)

spell = concept.to_spell([runes.double_damage_rune])
lightning_active = Active.from_spell(spell)

