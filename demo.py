from DreamGame import DreamGame
from content.base_types.demo_hero import demohero_basetype
from content.dungeons.demo_dungeon import demo_dungeon
from game_objects.battlefield_objects import Unit

game = DreamGame.start_dungeon(demo_dungeon, Unit(demohero_basetype))
print(game)
print(dir(demo_dungeon))
print(demo_dungeon.unit_locations)
for unit, position in demo_dungeon.unit_locations.items():
    print(unit.is_obstacle)
    # print(key.icon)
    # print(item)
# print(demo_dungeon.hero_entrance)
# print(demo_dungeon.w, demo_dungeon.h)
time = game.loop()
print(dir(time))
