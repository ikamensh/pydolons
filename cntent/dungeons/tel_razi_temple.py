from battlefield.Battlefield import Cell
from cntent.monsters.tel_razi.monsters import golem, tel_razi_scrub, tel_razi_zealot
from game_objects.dungeon.Dungeon import Dungeon
from mechanics.factions import Faction


def build_unit_locations(g):
    tel_band = [golem.create(g, 3+3j),
                golem.create(g, 6+6j),
                tel_razi_scrub.create(g, 3+6j),
                tel_razi_zealot.create(g, 4+4j)]
    return tel_band


tel_razi_temple = Dungeon("Tel'Razi Temple", 9, 9,
                          objs=build_unit_locations,
                          hero_entrance=Cell(8, 4), icon="wormface2.jpg")
