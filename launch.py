# import game_loop object and ProxyEmit
from GameLoopThread import GameLoopThread, ProxyEmit
from character_creation.Character import Character
from mechanics.AI.SimGame import SimGame as DreamGame
from content.base_types.demo_hero import demohero_basetype
from content.dungeons.demo_dungeon import demo_dungeon
from game_objects.battlefield_objects import Unit
from ui.TheUI import TheUI
from threading import Thread
# import triggers
from ui.triggers.animation_triggers import move_anim_trigger, damage_anim_trigger, attack_anin_trigger, perish_anim_trigger, turn_anim_trigger, nexunit_anim_trigger, levelstatus_trigger

import time

import sys

from PySide2 import QtCore, QtGui, QtWidgets


def one_game():
    """

    DO NOT MODIFY THIS FILE!

    """
    # Qt application initialization
    app = QtWidgets.QApplication(sys.argv)
    # Logical engine initialization
    game = DreamGame.start_dungeon(demo_dungeon, Unit(demohero_basetype))
    game.character = Character(demohero_basetype)
    # Ui engine initialization
    window = TheUI(game)
    TheUI.singleton = window

    # NEW TRIGGER ADD THIS |
    #
    levelstatus_trigger(),
    nexunit_anim_trigger(),
    turn_anim_trigger(),
    perish_anim_trigger(),
    attack_anin_trigger(),
    damage_anim_trigger(),
    move_anim_trigger()


    # debug print
    game.print_all_units()
    # game_loop thread initialization
    loop = GameLoopThread()
    # set game and ui engine
    loop.game = game
    loop.the_ui = window
    # Qt signal initialization
    loop.setSiganls(ProxyEmit)
    # if the game_loop completes work then thread will completes its work
    loop.start()
    # debug time sleep
    # time.sleep(5)
    # debug print
    print(f"battle lasted for {time}")
    # Qt application exit
    sys.exit(app.exec_())


one_game()

# from cProfile import Profile
# profiler = Profile()
# profiler.runcall(one_game)
# profiler.print_stats('cumulative')
