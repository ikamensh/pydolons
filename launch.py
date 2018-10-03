from GameLoopThread import GameLoopThread, ProxyEmit
from mechanics.AI.SimGame import SimGame as DreamGame
from content.base_types.demo_hero import demohero_basetype
from content.dungeons.demo_dungeon import demo_dungeon
from game_objects.battlefield_objects import Unit
from ui.TheUI import TheUI
from threading import Thread
from ui.triggers.animation_triggers import move_anim_trigger, damage_anim_trigger

import time

import sys

from PySide2 import QtCore, QtGui, QtWidgets


def one_game():
    app = QtWidgets.QApplication(sys.argv)
    game = DreamGame.start_dungeon(demo_dungeon, Unit(demohero_basetype))
    window = TheUI(game)
    TheUI.singleton = window

    damage_anim_trigger(),
    move_anim_trigger()

    game.print_all_units()

    loop = GameLoopThread()
    loop.game = game
    loop.the_ui = window
    loop.setSiganls(ProxyEmit)
    loop.start()

    time.sleep(5)

    print(f"battle lasted for {time}")
    sys.exit(app.exec_())

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
