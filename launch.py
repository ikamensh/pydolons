# import game_loop object and ProxyEmit
from GameLoopThread import GameLoopThread, ProxyEmit
from character_creation.Character import Character
from mechanics.AI.SimGame import SimGame as DreamGame
from cntent.base_types.demo_hero import demohero_basetype
from cntent.dungeons.demo_dungeon import demo_dungeon
from cntent.dungeons.demo_dungeon_walls import walls_dungeon
from cntent.dungeons.pirate_lair import pirate_lair
from cntent.dungeons.small_graveyard import small_graveyard
from cntent.dungeons.small_orc_cave import small_orc_cave

from ui.TheUI import TheUI
# import triggers
from ui.triggers.animation_triggers import move_anim_trigger, damage_anim_trigger, attack_anin_trigger, \
    perish_anim_trigger, turn_anim_trigger, nexunit_anim_trigger, levelstatus_trigger, ui_error_message_trigger

import time
from datetime import datetime

import sys

from PySide2 import QtCore, QtGui, QtWidgets


def one_game():
    """

    DO NOT MODIFY THIS FILE!

    """
    # Qt application initialization
    app = QtWidgets.QApplication(sys.argv)
    # The_hero character init
    character  = Character(demohero_basetype)
    # Logical engine initialization, the_hero create from character
    print('cfg ===> start init DreamGame', datetime.now())
    # game = DreamGame.start_dungeon(walls_dungeon, character.unit)
    game = DreamGame.start_dungeon(small_orc_cave, character.unit)
    print('cfg ===> init DreamGame', datetime.now())
    # add character field for game
    game.character = character
    # Ui engine initialization
    window = TheUI(game)
    TheUI.singleton = window

    # NEW TRIGGER ADD THIS |
    #
    levelstatus_trigger(),
    ui_error_message_trigger(),
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
    # example correct stop thread
    def close_app():
        # game.loop stop condition
        game.loop_state = False
        # thread call quit, exit from thread
        loop.quit()
        # application waiting for shutdown thread
        loop.wait()

    # call exit from window
    app.aboutToQuit.connect(close_app)
    # set game and ui engine
    loop.game = game
    loop.the_ui = window
    # Qt signal initialization
    loop.setSiganls(ProxyEmit)
    # if the game_loop completes work then thread will completes its work
    loop.start()
    sys.exit(app.exec_())


one_game()

# from cProfile import Profile
# profiler = Profile()
# profiler.runcall(one_game)
# profiler.print_stats('cumulative')
