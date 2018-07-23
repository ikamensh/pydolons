from mechanics.damage import DamageEvent, Damage, DamageTypes
from content.spells import runes
from game_objects.spells import  SpellConcept
from character_creation.MasteriesEnum import MasteriesEnum
from mechanics.actives import SingleUnitTargeting, Costs, Active
from game_objects.spells import Rune, SpellAttributes
from game_objects.attributes import Bonus, Attribute
import pytest





@pytest.fixture()
def double_damage_rune():
    __double_damage_bonus = Bonus({SpellAttributes.AMOUNT: Attribute(0, 100, 0)})
    __complexity_cost_bonus = Bonus({SpellAttributes.COMPLEXITY: Attribute(0, 0, 20)})

    _double_damage_rune = Rune([__double_damage_bonus, __complexity_cost_bonus])
    return _double_damage_rune

@pytest.fixture()
def lightning_bolt_callback():
    def _lightning_bolt_callback(active, single_unit_targeting):
        source = active.owner
        target = single_unit_targeting.unit

        spell = active.spell
        n_damage = spell.amount
        dmg = Damage(n_damage, DamageTypes.LIGHTNING)

        DamageEvent(dmg, target=target, source=source)
    return _lightning_bolt_callback


@pytest.fixture()
def lightning_concept(lightning_bolt_callback):
    concept = SpellConcept(name="lightning bolt",
                       school=MasteriesEnum.LIGHTNING,
                       targeting_cls=SingleUnitTargeting,
                       complexity=30,
                       costs=Costs(4, 40, 0, readiness=1),
                       amount=60, duration=None, precision_factor=1,
                       distance=5, radius=None,
                       resolve_callback=lightning_bolt_callback)
    return concept

@pytest.fixture()
def lightning_spell_dd(lightning_concept):
    spell = lightning_concept.to_spell([runes.double_damage_rune])
    return spell

@pytest.fixture()
def lightning_active(lightning_spell_dd):
    active = Active.from_spell(lightning_spell_dd)
    return active