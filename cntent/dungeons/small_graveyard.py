from battlefield.Battlefield import Cell
from cntent.monsters.undead import skeleton, zombie
from game_objects.dungeon.Dungeon import Dungeon

def build_unit_locations():
    pirate_band = [skeleton.create() for _ in range(3)] + [zombie.create() for _ in range(2)]
    locations = [Cell(1,1), Cell(1,7), Cell(4, 4), Cell(4, 5), Cell(5, 4)]
    unit_locations = {pirate_band[i]: locations[i] for i in range(5)}
    return unit_locations



small_graveyard = Dungeon(build_unit_locations, 8, 8, hero_entrance=Cell(3, 4))
