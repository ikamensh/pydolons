from battlefield.Battlefield import Cell
from cntent.monsters.undead import skeleton, zombie
from game_objects.dungeon.Dungeon import Dungeon

def build_unit_locations(g):
    pirate_band = [skeleton.create(g) for _ in range(2)] + [zombie.create(g) for _ in range(1)]
    locations = [Cell(1,1), Cell(1,7), Cell(4, 4), Cell(4, 5), Cell(5, 4)]
    unit_locations = {pirate_band[i]: locations[i] for i in range(3)}
    return unit_locations



small_graveyard = Dungeon("Haunted Graveyard", 8, 8,unit_locations=build_unit_locations, hero_entrance=Cell(3, 4), icon="undead.jpg")
