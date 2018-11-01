# import game_loop object and ProxyEmit
from GameLoopThread import GameLoopThread, ProxyEmit
from character.Character import Character
from mechanics.AI.SimGame import SimGame as DreamGame
from cntent.base_types.demo_hero import demohero_basetype
from cntent.dungeons.demo_dungeon import demo_dungeon
from cntent.dungeons.demo_dungeon_walls import walls_dungeon
from game_objects.battlefield_objects import Unit
from ui.TheUI import TheUI
from threading import Thread
# import triggers
from ui.triggers.animation_triggers import move_anim_trigger, damage_anim_trigger, attack_anin_trigger, \
    perish_anim_trigger, turn_anim_trigger, nexunit_anim_trigger, levelstatus_trigger, ui_error_message_trigger

from single_player.Adventure import Adventure
from single_player.Mission import Mission

import time

import sys

from PySide2 import QtCore, QtGui, QtWidgets


def adventure_game():


    mission = Mission([demo_dungeon, walls_dungeon])
    adventure = Adventure(demohero_basetype, mission)

    for dungeon in adventure.first_mission:
        hero_unit = adventure.character.unit
        game = DreamGame.start_dungeon(dungeon, hero_unit)
        game.character = adventure.character # TODO remove?

        app = QtWidgets.QApplication(sys.argv)

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

        #TODO does not work this way
        result = game.loop()

        if result != "VICTORY":
            print("you have lost the game.")
            return "DEFEAT"
        adventure.character.update(hero_unit)

    return "VICTORY"




adventure_game()

# from cProfile import Profile
# profiler = Profile()
# profiler.runcall(one_game)
# profiler.print_stats('cumulative')
