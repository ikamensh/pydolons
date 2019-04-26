import pytest
from character import Character, MasteriesEnum
from cntent.base_types import pirate_basetype

@pytest.fixture()
def char():
    c = Character(pirate_basetype)
    return c

@pytest.fixture(params=MasteriesEnum)
def var_mastery(request):
    yield request.param


@pytest.fixture()
def one_mastery():
    yield MasteriesEnum.SWORD