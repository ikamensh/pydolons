from battlefield.Battlefield import Cell
from cntent.monsters.greenskins import goblin, orc, ogre
from game_objects.dungeon.Dungeon import Dungeon


def build_unit_locations():
    orcs_band = [goblin.create(), orc.create(), ogre.create()]
    locations = [Cell(3, 3), Cell(6, 6), Cell(3, 6)]
    unit_locations = {orcs_band[i]: locations[i] for i in range(3)}
    return unit_locations


small_orc_cave = Dungeon(build_unit_locations, 8, 8, hero_entrance=Cell(3, 4))
