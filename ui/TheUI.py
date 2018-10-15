import sys

from PySide2 import QtCore, QtGui, QtWidgets

from ui.GameRootNode import GameRootNode

from ui.GameAnimation import Animations
from ui.GamePages import GamePages
from ui.GamePages.suwidgets.SuWidgetFactory import SuWidgetFactory

from ui.GameController import GameController
from ui.levels import Level_demo_dungeon

from ui.GameView import GameView

from datetime import datetime

class TheUI(QtWidgets.QWidget):
    view = None
    singleton = None

    def __init__(self, game):
        super().__init__()
        print('cfg ===> start init TheUI', datetime.now())
        self.game = game
        self.gameTimer = QtCore.QTimer()
        self.gameTimer.timeout.connect(self.timerSlot)
        self.gameTimer.startTimer(int(1000 / 50))

        cursor = QtGui.QCursor(QtGui.QPixmap('resources/assets/ui/cursor.png'))
        self.setCursor(cursor)

        self.gameRoot: GameRootNode = GameRootNode()
        self.gameRoot.game = self.game

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

        self.controller = GameController(self.game)
        self.gameRoot.setGameController(self.controller)

        self.level = Level_demo_dungeon(self.gameconfig)
        self.gameRoot.setLevel(self.level)
        self.level.setUpLevel(self.game, self.controller)

        self.scene.addItem(self.level.world)
        self.scene.addItem(self.level.units)
        self.scene.addItem(self.level.middleLayer)
        self.scene.addItem(self.controller.cursor)

        self.gamePages = GamePages()
        self.gameRoot.setGamePages(self.gamePages)
        self.gamePages.setUpPages()
        self.gamePages.setHeroUnit(self.game.the_hero)
        self.gamePages.setCharacter(self.game.character)
        self.view.resized.connect(self.gamePages.updateGui)

        self.view.controller = self.controller
        self.view.setScene(self.scene)

        self.showMaximized()
        print('cfg ===> init TheUI', datetime.now())




    def changeTo(self):
        self.scene.update(-self.gameconfig.ava_ha_size[0],
                          -self.gameconfig.ava_ha_size[1],
                          self.gameconfig.ava_size[0],
                          self.gameconfig.ava_size[1])


    def timerSlot(self):
        print('timerSlot')


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
