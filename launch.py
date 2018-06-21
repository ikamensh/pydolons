from dungeon.dungeons.demo_dungeon import demo_dungeon
from Game import Game
from game_objects.battlefield_objects.Unit.base_types.demo_hero import demohero_basetype
from game_objects.battlefield_objects.Unit.Unit import Unit

game = Game(demo_dungeon, Unit(demohero_basetype))
print(game)
game.print_all_units()
game.loop()