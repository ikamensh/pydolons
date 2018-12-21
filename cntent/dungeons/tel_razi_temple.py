from battlefield.Battlefield import Cell
from cntent.monsters.tel_razi.monsters import golem, tel_razi_scrub, tel_razi_zealot
from game_objects.dungeon.Dungeon import Dungeon


def build_unit_locations(g):
    tel_band = [golem.create(g), golem.create(g), tel_razi_scrub.create(g), tel_razi_zealot.create(g)]
    locations = [Cell(3, 3), Cell(6, 6), Cell(3, 6), Cell(4,4)]
    unit_locations = {tel_band[i]: locations[i] for i in range(4)}
    return unit_locations


tel_razi_temple = Dungeon("Tel'Razi Temple", 9, 9, unit_locations=build_unit_locations, hero_entrance=Cell(8, 4), icon="wormface2.jpg")
