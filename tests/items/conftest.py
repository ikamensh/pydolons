import pytest

from game_objects.items import WeaponBlueprint, WeaponTypes, Material, MaterialTypes, ArmorTypes, ArmorBlueprint
from game_objects.items import QualityLevel
from game_objects.items import  BodyArmor, Weapon
from mechanics.damage import Damage, DamageTypes, Armor


@pytest.fixture()
def bronze():
    return Material(MaterialTypes.METAL, "bronze", 0.5)

@pytest.fixture()
def silver():
    return Material(MaterialTypes.METAL, "bronze", 1.1)

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
    return WeaponBlueprint("sword", weapon_type=WeaponTypes.SWORD, material_type=MaterialTypes.METAL, rarity=1)

@pytest.fixture()
def my_cuirass_blueprint():
    return ArmorBlueprint("cuirass", target_item_type=ArmorTypes.CUIRASS, rarity=1)

@pytest.fixture()
def real_weapon(my_sword_blueprint, bronze, usual, empty_game):
    return Weapon("test axe1", Damage(50, DamageTypes.SLASH), max_durability=50,
                  blueprint=my_sword_blueprint, material=bronze, quality=usual,
                  game=empty_game, is_ranged=False)

def _weapon(empty_game):
    return Weapon("test axe1", Damage(50, DamageTypes.SLASH),
                  max_durability=50, game=empty_game, is_ranged=False)

@pytest.fixture()
def weapon(empty_game):
    return _weapon(empty_game)



def _armor(empty_game):
    return BodyArmor("da armor", Armor(30), max_durability=50, game=empty_game)


@pytest.fixture()
def armor(empty_game):
    return _armor(empty_game)

@pytest.fixture(params=[_weapon, _armor])
def diff_item(request, empty_game):
    item = request.param(empty_game)
    yield item

from cntent.items.std.std_ranged import black_bow, cadamba_crossbow

@pytest.fixture()
def bow():
    return black_bow

@pytest.fixture()
def crossbow():
    return cadamba_crossbow