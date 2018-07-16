import pytest

from game_objects.items import WeaponBlueprint, WeaponTypes, Material, MaterialTypes, ArmorTypes, ArmorBlueprint
from game_objects.items.blueprints.QualityLevels import QualityLevel
from game_objects.items import  BodyArmor, Weapon
from mechanics.damage import Damage, DamageTypes, Armor


@pytest.fixture()
def bronze():
    return Material(MaterialTypes.METAL, "bronze", 0.5)

@pytest.fixture()
def troll_skin():
    return Material(MaterialTypes.SKIN, "Black Troll Hide", 1.4)

@pytest.fixture()
def usual():
    return QualityLevel("usual", 1)

@pytest.fixture()
def legendary():
    return QualityLevel("legendary", 2)

@pytest.fixture()
def my_sword_blueprint():
    return WeaponBlueprint("sword", item_type=WeaponTypes.SWORD, material_type=MaterialTypes.METAL, rarity=1)

@pytest.fixture()
def my_cuirass_blueprint():
    return ArmorBlueprint("cuirass", item_type=ArmorTypes.CUIRASS, rarity=1)

@pytest.fixture()
def weapon():
    return Weapon("test axe1", Damage(5, DamageTypes.SLASH), 5, None, None, None)

@pytest.fixture()
def armor():
    return BodyArmor("da armor", Armor(3), 3, None, None, None)

@pytest.fixture(params=[weapon, armor])
def diff_item(request):
    item = request.param()
    yield item