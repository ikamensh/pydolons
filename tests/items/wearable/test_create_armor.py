import pytest
from mechanics.damage import DamageTypes


def test_create_blueprint(my_cuirass_blueprint):
    assert my_cuirass_blueprint.armor is not None

def test_create_item(bronze, usual, my_cuirass_blueprint):
    my_cuirass = my_cuirass_blueprint.to_item(bronze, usual)
    assert my_cuirass.armor[DamageTypes.FIRE] < my_cuirass_blueprint.armor[DamageTypes.FIRE]


def test_wrong_type(troll_skin, usual, my_cuirass_blueprint):
    with pytest.raises(AssertionError):
        my_cuirass = my_cuirass_blueprint.to_item(troll_skin, usual)
