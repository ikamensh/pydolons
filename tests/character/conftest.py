import pytest
from character import Character, MasteriesEnum
from cntent.base_types import pirate_basetype
from game_objects.battlefield_objects.CharAttributes import core_attributes
from game_objects.battlefield_objects import CharAttributes

@pytest.fixture()
def char():
    c = Character(pirate_basetype)
    return c

@pytest.fixture()
def char_with_xp():
    c = Character(pirate_basetype)
    c.unit.xp = int(1e100)
    return c

@pytest.fixture(params=MasteriesEnum)
def var_mastery(request):
    yield request.param


@pytest.fixture()
def some_mastery():
    yield MasteriesEnum.SWORD

@pytest.fixture()
def some_attribute():
    yield CharAttributes.STREINGTH

@pytest.fixture(params=core_attributes)
def var_attribute(request):
    yield request.param