from cntent.abilities.generic import fat

from game_objects.battlefield_objects import BaseType
from game_objects.monsters.Monster import Monster



zombie_norm = BaseType({},"Zombie")
zombie_fat = BaseType({},"Zombie", abilities=[fat])

zombie_norm = Monster(zombie_norm)
zombie_fat = Monster(zombie_fat)



def test_fat():

    z_norm = zombie_norm.create()
    z_fat = zombie_fat.create()

    assert z_norm.health < z_fat.health
    assert z_norm.initiative > z_fat.initiative
