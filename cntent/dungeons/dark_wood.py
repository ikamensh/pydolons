from battlefield import Cell
from cntent.monsters.werewolves import werewolf
from game_objects.dungeon.Dungeon import Dungeon


def build_units(g):
    werewolf_band = [werewolf.create(g, 3+3j),
                     werewolf.create(g, 6+6j),
                     werewolf.create(g, 3+6j)]
    return werewolf_band


dark_wood = Dungeon("Dark Wood", 8, 8,
                    construct_objs=build_units,
                    hero_entrance=Cell(3, 4),
                    icon="dark_wood.jpg")