from battlefield.Battlefield import Cell
from cntent.base_types import mud_golem_basetype
from cntent.monsters.pirates import pirate_scum
from game_objects.battlefield_objects import Unit
from game_objects.dungeon.Dungeon import Dungeon
from mechanics.factions import Faction


def create_monsters(g):
    monsters = [pirate_scum.create(g, Cell(4, 4)),
                pirate_scum.create(g, Cell(4, 5)),
                pirate_scum.create(g, Cell(5, 4)),
                Unit(mud_golem_basetype, cell=Cell(3, 3))]
    return monsters


demo_dungeon = Dungeon(
    "Pirate Bar",
    16,
    16,
    construct_objs=create_monsters,
    hero_entrance=Cell(
        3,
        4),
    icon="pirates_1.jpg")
