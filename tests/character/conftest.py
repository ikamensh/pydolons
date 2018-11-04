import pytest
from character.Character import Character
from cntent.base_types import pirate_basetype

@pytest.fixture()
def char():
    c = Character(pirate_basetype)
    return c