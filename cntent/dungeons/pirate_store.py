from battlefield.Battlefield import Cell
from game_objects.battlefield_objects import Wall
from game_objects.dungeon.Dungeon import Dungeon
from cntent.monsters.pirates import pirate_scum, pirate_boatswain, pirate_captain


def green_group(g, x, y):
    return {pirate_scum.create(g): Cell(x, y)}


def yellow_group(g, x, y):
    return {pirate_scum.create(g): Cell(x, y),
            pirate_scum.create(g): Cell(x, y)}


def orange_group(g, x, y):
    return {pirate_boatswain.create(g): Cell(x, y),
            pirate_boatswain.create(g): Cell(x, y),
            pirate_boatswain.create(g): Cell(x, y)}


def red_group(g, x, y):
    return {pirate_boatswain.create(g): Cell(x, y),
            pirate_boatswain.create(g): Cell(x, y),
            pirate_captain.create(g): Cell(x, y),
            pirate_captain.create(g): Cell(x, y)}


def create_units(g):
    unit_locations = {}
    place = """
_|_|W|_|_|_|_|_|_|_|_|_|_|_|_|_|
_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
_|_|W|W|W|W|W|W|W|W|W|W|W|W|_|_|
_|_|G|_|_|W|_|_|_|_|_|_|_|W|_|_|
_|_|W|_|W|_|O|W|_|_|Y|W|_|W|_|_|
_|_|W|W|W|_|_|_|_|_|_|_|_|W|_|_|
_|_|W|_|_|_|_|_|_|_|W|G|W|W|_|_|
_|Y|W|_|_|_|_|W|_|_|W|_|_|_|_|_|
_|_|W|_|_|W|_|_|_|_|W|_|_|_|_|_|
_|_|W|_|_|_|_|_|_|_|W|_|_|_|_|_|
_|_|W|W|W|_|_|_|_|W|W|W|W|W|_|_|
_|_|G|_|W|_|_|_|_|G|_|_|_|W|_|_|
_|_|W|_|W|_|_|_|_|W|_|R|_|W|_|_|
_|_|W|W|W|W|W|W|W|W|_|_|_|W|_|_|
_|_|_|_|_|_|_|_|_|G|_|_|_|W|_|_|
_|_|_|_|W|W|W|W|W|W|_|_|_|W|_|_|
"""
    words = {'G': green_group, 'Y': yellow_group, 'O': orange_group, 'R': red_group}
    y = 0
    for s in place.split('\n'):
        if len(s) > 6:
            x = 0
            for w in s:
                func = words.get(w)
                if func is not None:
                    unit_locations.update(func(g, int(x/2+0.5), y))
                x += 1
            y += 1
    for u, c in unit_locations.items():
        u.cell = c
    return list(unit_locations.keys())


def create_walls():
    place = """
_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
_|_|W|W|W|W|W|W|W|W|W|W|W|W|_|_|
_|_|G|_|_|W|_|_|_|_|_|_|_|W|_|_|
_|_|W|_|W|_|O|W|_|_|Y|W|_|W|_|_|
_|_|W|W|W|_|_|_|_|_|_|_|_|W|_|_|
_|_|W|_|_|_|_|_|_|_|W|G|W|W|_|_|
_|Y|W|_|_|_|_|W|_|_|W|_|_|_|_|_|
_|_|W|_|_|W|_|_|_|_|W|_|_|_|_|_|
_|_|W|_|_|_|_|_|_|_|W|_|_|_|_|_|
_|_|W|W|W|_|_|_|_|W|W|W|W|W|_|_|
_|_|G|_|W|_|_|_|_|G|_|_|_|W|_|_|
_|_|W|_|W|_|_|_|_|W|_|R|_|W|_|_|
_|_|W|W|W|W|W|W|W|W|_|_|_|W|_|_|
_|_|_|_|_|_|_|_|_|G|_|_|_|W|H|_|
_|_|_|_|W|W|W|W|W|W|_|_|_|W|_|_|
"""
    walls = []
    y = 0
    for s in place.split('\n'):
        if len(s) > 6:
            x = 0
            for w in s:
                if w == 'W':
                    walls.append(Wall(cell=Cell(int(x/2+0.5), y)))
                x += 1
            y += 1
    return walls


pirate_store = Dungeon("Pirate Store", 16, 16,
                      construct_objs=create_units,
                      construct_walls=create_walls,
                      hero_entrance=Cell(8, 6),
                      icon="pirates_3.jpg")

if __name__ == '__main__':
    place ="""
_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
_|_|W|W|W|W|W|W|W|W|W|W|W|W|_|_|
_|_|G|_|_|W|_|_|_|_|_|_|_|W|_|_|
_|_|W|_|W|_|_|W|_|_|Y|W|_|W|_|_|
_|_|W|W|W|_|_|_|_|_|_|_|_|W|_|_|
_|_|W|_|_|_|_|_|_|_|W|G|W|W|_|_|
_|Y|W|_|_|Y|_|W|_|_|W|_|_|_|_|_|
_|_|W|_|_|W|_|_|_|_|W|_|_|_|_|_|
_|_|W|_|_|_|_|_|_|_|W|_|_|_|_|_|
_|_|W|W|W|_|_|O|_|W|W|W|W|W|_|_|
_|_|G|_|W|_|_|_|_|G|_|_|_|W|_|_|
_|_|W|_|W|_|_|_|_|W|_|R|_|W|_|_|
_|_|W|W|W|W|W|W|W|W|_|_|_|W|_|_|
_|_|_|_|_|_|_|_|_|G|_|_|_|W|H|_|
_|_|_|_|W|W|W|W|W|W|_|_|_|W|_|_|
"""
    # print(place.split('\n'))
    words = ['W','G','R','Y','O','H']
    y = 0
    for s in place.split('\n'):
        if len(s) > 6:
            x = 0
            for w in s:
                if w in words:
                    print(w, int(x/2+0.5),y)
                x += 1
            y += 1

