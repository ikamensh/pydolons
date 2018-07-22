from game_objects.battlefield_objects.attributes import Bonus
from game_objects.spells import Spell, SpellAttributes, SpellConcept, Rune
from mechanics.actives import Costs

import pytest

@pytest.fixture()
def usual_costs():
    return Costs(2, 10)

