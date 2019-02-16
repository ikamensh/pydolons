from battlefield.Battlefield import Cell
from cntent.monsters.werewolves import werewolf
from game_objects.dungeon.Dungeon import Dungeon


def build_unit_locations(g):
    werewolf_band = [werewolf.create(g), werewolf.create(g), werewolf.create(g)]
    locations = [Cell(3, 3), Cell(6, 6), Cell(3, 6)]
    unit_locations = {werewolf_band[i]: locations[i] for i in range(3)}
    return unit_locations


dark_wood = Dungeon("Dark Wood", 8, 8, unit_locations=build_unit_locations, hero_entrance=Cell(3, 4), icon="dark_wood.jpg")