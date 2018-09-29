from mechanics.AI.SimGame import SimGame as DreamGame
from content.base_types.demo_hero import demohero_basetype
from content.dungeons.demo_dungeon import demo_dungeon
from game_objects.battlefield_objects import Unit
from ui.TheUI import TheUI
from threading import Thread
from ui.sounds.sound_triggers import attack_sounds_trig, damage_sounds_trig, move_sounds_trig, perish_sounds_trig

from time import time


def one_game():
    game = DreamGame.start_dungeon(demo_dungeon, Unit(demohero_basetype))

    # attack_sounds_trig(),
    # damage_sounds_trig(),
    move_sounds_trig(),
    # perish_sounds_trig()

    print(game)
    game.print_all_units()
    Thread(target=TheUI.launch, args=[game]).start()
    time = game.loop()
    print(f"battle lasted for {time}")

# t = time()
#
# one_game()
#
# print(f"it took {time()-t} sec of real time.")

one_game()

# from cProfile import Profile
#
# profiler = Profile()
# profiler.runcall(one_game)
#
# profiler.print_stats('cumulative')
