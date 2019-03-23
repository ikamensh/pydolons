from battlefield.Battlefield import Cell
from cntent.monsters.tel_razi.monsters import golem, sentinel
from game_objects.dungeon.Dungeon import Dungeon
from mechanics.factions import Faction



def build_unit_locations(g):

    monsters = [sentinel.create(g, 5+5j),
                      sentinel.create(g, 5 + 6j),
                      golem.create(g, 6 + 5j),
                      golem.create(g, 6 + 6j),
                      golem.create(g, 4 + 5j),
                      golem.create(g, 4 + 6j)]

    for m in monsters:
        m.faction = Faction.ENEMY

    return monsters


tel_razi_factory = Dungeon("Tel'Razi Factory", 9, 9,
                           objs=build_unit_locations,
                           hero_entrance=Cell(8, 4),
                           icon="sentinel.jpg")
