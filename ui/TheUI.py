import sys


from PySide2 import QtCore, QtGui, QtWidgets

from ui.GameRootNode import GameRootNode

from ui.GameAnimation import Animations
from ui.GamePages import GamePages
from ui.GamePages.suwidgets.SuWidgetFactory import SuWidgetFactory

from ui.GameController import GameController
from ui.levels import LevelFactory

from ui.GameView import GameView

from LEngine import LEngine
from GameLoopThread import GameLoopThread, ProxyEmit



from datetime import datetime

class TheUI(QtWidgets.QWidget):
    view = None
    singleton = None

    def __init__(self, lengine:LEngine, game = None):
        super().__init__()
        print('cfg ===> start init TheUI', datetime.now())
        # work level
        self.lengine = lengine
        self.loop = None

        self.gameTimer = QtCore.QTimer()
        self.gameTimer.timeout.connect(self.timerSlot)
        self.gameTimer.startTimer(int(1000 / 50))

        cursor = QtGui.QCursor(QtGui.QPixmap('resources/assets/ui/cursor.png'))
        self.setCursor(cursor)

        self.gameRoot: GameRootNode = GameRootNode()
        self.gameRoot.lengine = self.lengine

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.view = GameView(self)
        self.gameRoot.setView(self.view)
        self.gameRoot.suwidgetFactory = SuWidgetFactory

        self.gameconfig = self.view.gameconfig
        self.gameconfig.animations = Animations()
        self.gameRoot.setGameConfig(self.view.gameconfig)
        self.layout.addWidget(self.view)
        self.layout.setMargin(2)

        self.scene = QtWidgets.QGraphicsScene(0, 0, 500, 500)
        self.gameRoot.setScene(self.scene)
        self.scene.setFocus(focusReason=QtCore.Qt.OtherFocusReason)
        self.scene.setBackgroundBrush(QtGui.QBrush(self.gameconfig.getPicFile('dungeon.jpg')))

        self.controller = GameController()
        self.gameRoot.setGameController(self.controller)

        self.levelFactory = LevelFactory(self.lengine)
        self.gameRoot.setLevelFactory(self.levelFactory)

        self.gamePages = GamePages()
        self.gameRoot.setGamePages(self.gamePages)
        self.gamePages.setUpStartPage(self)

        self.view.resized.connect(self.gamePages.resized)
        self.view.setScene(self.scene)

        self.showMaximized()
        print('cfg ===> init TheUI', datetime.now())




    def changeTo(self):
        self.scene.update(-self.gameconfig.ava_ha_size[0],
                          -self.gameconfig.ava_ha_size[1],
                          self.gameconfig.ava_size[0],
                          self.gameconfig.ava_size[1])

    def initLevel(self, level_name = None):
        self.level = self.levelFactory.getLevel(level_name)
        self.levelFactory.addLevelToScene(self.scene)

    def destroyLevel(self):
        self.levelFactory.removeLevelFromScene(self.scene)

    def timerSlot(self):
        print('timerSlot')

    def close_app(self):
        if not self.loop is None:
            self.stopGame()


    def startGame(self):
        self.loadGame()
        # debug print
        # self.game.print_all_units()
        # game_loop thread initialization
        self.loop = GameLoopThread()
        # set game and ui engine
        self.loop.game = self.game
        self.loop.the_ui = self
        # Qt signal initialization
        self.loop.setSiganls(self.proxyEmit)
        # if the game_loop completes work then thread will completes its work
        self.loop.start()

    def loadGame(self):
        ####################################################
        #                                                  #
        #  change level this                               #
        #                vvvvvvvvvvvvvvvvvvv               #
        ####################################################
        self.game = self.lengine.getGame('demo_level')
        # self.game = lengine.getGame('small_graveyard_level')
        # self.game = lengine.getGame('small_orc_cave_level')
        # self.game = lengine.getGame('walls_level')
        # self.game = lengine.getGame('pirate_level')
        self.gameRoot.game = self.game
        self.initLevel()
        self.gamePages.setUpPages()
        self.gamePages.setHeroUnit(self.game.the_hero)
        self.gamePages.setCharacter(self.game.character)
        self.view.controller = self.controller



    def stopGame(self):
        # game.loop stop condition
        self.game.loop_state = False
        # thread call quit, exit from thread
        self.loop.quit()
        # application waiting for shutdown thread
        self.loop.wait()

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
    from mechanics.AI.SimGame import SimGame as DreamGame
    from cntent.base_types.demo_hero import demohero_basetype
    from cntent.dungeons.demo_dungeon import demo_dungeon
    from game_objects.battlefield_objects import Unit

    from threading import Thread



    game = DreamGame.start_dungeon(demo_dungeon, Unit(demohero_basetype))
    Thread(target=game.loop).start()

    app = QtWidgets.QApplication(sys.argv)
    window = TheUI(game)
    sys.exit(app.exec_())
