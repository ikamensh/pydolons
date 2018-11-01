from mechanics.damage import Damage, DamageTypes
from mechanics.events import DamageEvent
from cntent.spells import runes
from game_objects.spells import  SpellConcept
from character.masteries import MasteriesEnum
from mechanics.actives import Cost, Active
from game_objects.spells import Rune, SpellAttributes
from game_objects.attributes import Bonus, Attribute
from game_objects.battlefield_objects import BattlefieldObject
import pytest


@pytest.fixture()
def double_damage_rune():
    __double_damage_bonus = Bonus({SpellAttributes.AMOUNT: Attribute(0, 100, 0)})
    __complexity_cost_bonus = Bonus({SpellAttributes.COMPLEXITY: Attribute(0, 0, 20)})

    _double_damage_rune = Rune([__double_damage_bonus, __complexity_cost_bonus])
    return _double_damage_rune

@pytest.fixture()
def lightning_bolt_callback():
    def _lightning_bolt_callback(active, unit):
        source = active.owner
        target = unit

        spell = active.spell
        n_damage = spell.amount
        dmg = Damage(n_damage, DamageTypes.LIGHTNING)

        DamageEvent(dmg, target=target, source=source)
    return _lightning_bolt_callback


@pytest.fixture()
def lightning_concept(lightning_bolt_callback):
    concept = SpellConcept(name="lightning bolt",
                           school=MasteriesEnum.LIGHTNING,
                           targeting_cls=BattlefieldObject,
                           complexity=200,
                           cost=Cost(4, 40, 0, readiness=1),
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