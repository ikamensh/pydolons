from DreamGame import DreamGame
from content.base_types.demo_hero import demohero_basetype
from content.dungeons.demo_dungeon import demo_dungeon
from game_objects.battlefield_objects import Unit

from time import time


def one_game():
    game = DreamGame.start_dungeon(demo_dungeon, Unit(demohero_basetype))
    print(game)
    game.print_all_units()
    time = game.loop()
    print(f"battle lasted for {time}")

# t = time()
#
# one_game()
#
# print(f"it took {time()-t} sec of real time.")


from cProfile import Profile

profiler = Profile()
profiler.runcall(one_game)

profiler.print_stats('cumulative')




