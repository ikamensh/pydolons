from battlefield.Battlefield import Cell
from cntent.monsters.greenskins import goblin, orc, ogre
from game_objects.dungeon.Dungeon import Dungeon



def build_unit_locations(g):
    orcs_band = [goblin.create(g, 3+3j),
                 orc.create(g, 6+6j),
                 ogre.create(g, 3+6j)]
    return orcs_band


small_orc_cave = Dungeon("Greenskin's Cave", 8, 8, construct_objs=build_unit_locations, hero_entrance=Cell(3, 4), icon="greenskins.png")
