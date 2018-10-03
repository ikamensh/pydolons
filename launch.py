from mechanics.AI.SimGame import SimGame as DreamGame
from content.base_types.demo_hero import demohero_basetype
from content.dungeons.demo_dungeon import demo_dungeon
from game_objects.battlefield_objects import Unit
from ui.TheUI import TheUI
from threading import Thread
# from ui.sounds.sound_triggers import attack_sounds_trig, damage_sounds_trig, move_sounds_trig, perish_sounds_trig
from ui.triggers.animation_triggers import move_anim_trigger

import time

import sys

from PySide2 import QtCore, QtGui, QtWidgets

class WorkerOrder(QtCore.QThread):

    def __init__(self, parent=None):
        super(WorkerOrder, self).__init__(parent)
        self.game = None

    def run(self):
        self.game.loop()


def one_game():
    app = QtWidgets.QApplication(sys.argv)
    game = DreamGame.start_dungeon(demo_dungeon, Unit(demohero_basetype))
    window = TheUI(game)
    TheUI.singleton = window


    #attack_sounds_trig(),
    #damage_sounds_trig(),
    #move_sounds_trig(),
    #perish_sounds_trig()
    move_anim_trigger()

    print(game)
    game.print_all_units()

    # Thread(target=TheUI.launch, args=[game]).start()
    worker = WorkerOrder()
    worker.game = game
    worker.start()
    # Thread(target=game.loop).start()
    # TheUI.launch(game)
    time.sleep(5)
    print('game ready')
    # print(TheUI.singleton.gameRoot.cfg)
    # TheUI.singleton.gameRoot.cfg.sound_maps["SftStep3.wav"].play()
    # game.loop()

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
