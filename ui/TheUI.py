from __future__ import annotations

import sys

from PySide2 import QtCore, QtGui, QtWidgets

from ui.core import GameRootNode
from ui.core import GameController
from ui.core import GameView
from ui.core.levels import LevelFactory

from ui.animation import Animations
from ui.pages import GamePages

from LEngine import LEngine
from GameLoopThread import GameLoopThread, ProxyEmit

from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from DreamGame import DreamGame
    from ui.core.gameconfig.GameConfiguration import GameConfiguration
    from ui.core.levels.BaseLevel import BaseLevel


class TheUI(QtWidgets.QWidget):
    view = None
    singleton = None

    def __init__(self, lengine:LEngine, game = None):
        super().__init__()
        self.setAcceptDrops(True)
        print('cfg ===> newGame init TheUI', datetime.now())
        # work level
        self.lengine: LEngine = lengine
        self.loop: GameLoopThread = None

        cursor = QtGui.QCursor(QtGui.QPixmap('resources/assets/ui/cursor.png'))
        self.setCursor(cursor)

        self.gameRoot = GameRootNode()
        self.gameRoot.lengine = self.lengine
        self.gameRoot.ui = self

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.view = GameView(self)
        self.gameRoot.setView(self.view)

        self.gameconfig: GameConfiguration = self.view.gameconfig
        self.gameconfig.animations = Animations()
        self.gameRoot.setGameConfig(self.view.gameconfig)
        self.layout.addWidget(self.view)
        self.layout.setMargin(2)
        size: set = self.gameconfig.dev_cfg_size
        if size is not None:
            self.scene = QtWidgets.QGraphicsScene(0, 0, self.gameconfig.dev_cfg_size[0], self.gameconfig.dev_cfg_size[1])
        else:
            self.scene = QtWidgets.QGraphicsScene(0, 0, 500, 500)
        self.gameRoot.setScene(self.scene)
        self.scene.setFocus(focusReason=QtCore.Qt.OtherFocusReason)
        self.scene.setBackgroundBrush(QtCore.Qt.black)

        self.controller = GameController()
        self.gameRoot.setGameController(self.controller)

        self.levelFactory = LevelFactory(self.lengine)
        self.gameRoot.setLevelFactory(self.levelFactory)
        self.level: BaseLevel = None

        self.gamePages = GamePages()
        self.gameRoot.setGamePages(self.gamePages)
        self.gamePages.setUpStartPage(self)
        self.gamePages.setUpLevelsPage()
        self.gamePages.setUpReadmePage()
        self.gamePages.setUpSettingsPage()

        self.view.resized.connect(self.gamePages.resized)
        self.view.setScene(self.scene)
        self.window_config()
        print('cfg ===> init TheUI', datetime.now())

    def window_config(self):
        if self.gamePages.gameRoot.cfg.userConfig.read_config['window']['fullscreen']:
            self.showFullScreen()
        else:
            self.show()

    def changeTo(self):
        self.scene.update(-self.gameconfig.ava_ha_size[0],
                          -self.gameconfig.ava_ha_size[1],
                          self.gameconfig.ava_size[0],
                          self.gameconfig.ava_size[1])

    def initLevel(self, level_name = None):
        print('Iinit level')
        self.level  = self.levelFactory.getLevel()
        self.levelFactory.addLevelToScene(self.scene)

    def destroyLevel(self):
        print('Destroy level')
        self.levelFactory.removeLevelFromScene(self.scene)
        self.levelFactory.removeLevel()
        self.gameRoot.level = None

    def close_app(self):
        if not self.gameRoot.loop is None:
            self.stopGame()

    def setDefaultGame(self):
        self.gameRoot.game = self.lengine.getGame("Haunted Graveyard")
        # self.gameRoot.game = self.lengine.getGame('demo_level')
        # self.game = self.lengine.getGame('small_graveyard_level')
        # self.game = self.lengine.getGame('small_orc_cave_level')
        # self.game = self.lengine.getGame('walls_level')
        # self.game = self.lengine.getGame('pirate_level')

    def startCharacterPage(self):
        self.lengine.the_hero = self.lengine.getHero()
        self.gamePages.setUpCharecterPage()

    def startGame(self):
        self.gameRoot.game = self.lengine.getGame()
        self.loadGame()
        # game_loop thread initialization
        self.loop = GameLoopThread()
        self.gameRoot.loop = self.loop
        # set game and ui engine
        self.loop.game = self.gameRoot.game
        self.loop.the_ui = self
        # Qt signal initialization
        self.loop.setSiganls(ProxyEmit)
        # if the game_loop completes work then thread will completes its work
        self.loop.start()

    def loadGame(self):
        self.initLevel()
        self.gamePages.setUpPages()
        self.gamePages.resized()
        self.gamePages.page = self.gamePages.gameMenu
        self.view.controller = self.controller


    def stopGame(self):
        if not self.gameRoot.loop is None:
            # game.loop stop condition
            self.gameRoot.game.loop_state = False
            self.destroyLevel()
            self.gamePages.destroyPages()
            # thread call quit, exit from thread
            self.loop.quit()
            # application waiting for shutdown thread
            self.loop.wait(5000)
            del self.loop
            self.gameRoot.loop = None
            del self.gameRoot.game

    def pauseGame(self):
        pass

    def resumeGame(self):
        pass

    @staticmethod
    def launch(game):
        app = QtWidgets.QApplication(sys.argv)
        window = TheUI(game)
        TheUI.singleton = window
        sys.exit(app.exec_())


if __name__ == '__main__':
    from DreamGame import DreamGame
    from cntent.base_types.demo_hero import demohero_basetype
    from cntent.dungeons.demo_dungeon import demo_dungeon
    from game_objects.battlefield_objects import Unit

    from threading import Thread

    game = DreamGame.start_dungeon(demo_dungeon, Unit(demohero_basetype))
    Thread(target=game.loop).start()

    app = QtWidgets.QApplication(sys.argv)
    window = TheUI(game)
    sys.exit(app.exec_())
