from battlefield.Battlefield import Cell
from cntent.monsters.undead import skeleton, zombie
from game_objects.dungeon.Dungeon import Dungeon


def build_unit_locations(g):
    monsters = [skeleton.create(g, 1+1j),
                skeleton.create(g, 1+7j),
                zombie.create(g, 4+4j)]


    return monsters



small_graveyard = Dungeon("Haunted Graveyard", 8, 8, objs=build_unit_locations, hero_entrance=Cell(3, 4), icon="undead.jpg")
