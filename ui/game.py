import sys

from PySide2 import QtCore, QtGui, QtWidgets

from ui.menu import ScreenMenu
from ui.gamecontroller import GameController
from ui.levels import Level_demo_dungeon

from ui.GameConfiguration import GameConfiguration
from ui.NotMyView import MyView


class TheUI(QtWidgets.QWidget):
    """docstring for Window."""
    view = None
    def __init__(self, game):
        super().__init__()
        self.the_game = game
        self.gameconfig = GameConfiguration()
        self.setupUI()

    def setupUI(self):

        #  Timer
        self.gameTimer = QtCore.QTimer()
        self.gameTimer.timeout.connect(self.timerSlot)
        self.gameTimer.startTimer(int(1000/50))
        # Cursor
        cursor = QtGui.QCursor(QtGui.QPixmap('resources/assets/ui/cursor.png'))
        self.setCursor(cursor)
        #
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.view = MyView(self)
        self.layout.addWidget(self.view)
        self.layout.setMargin(2)
        # print(dir(self.layout))

        self.scene = QtWidgets.QGraphicsScene(-250, -250, 500, 500)
        self.scene.setFocus(focusReason = QtCore.Qt.OtherFocusReason)
        self.scene.setBackgroundBrush(QtGui.QBrush(self.gameconfig.getPicFile('dungeon.jpg')))
        self.view.setScene(self.scene)

        self.controller = GameController(self.gameconfig, self.the_game)
        self.controller.setView(self.view)
        self.controller.scene = self.scene

        self.level = Level_demo_dungeon(self.gameconfig)
        self.level.setController(self.controller)
        self.level.setUpLevel(self.the_game)
        self.scene.addItem(self.level.world)
        self.scene.addItem(self.level.units)
        self.scene.addItem(self.level.midleLayer)
        self.view.controller = self.controller
        self.showMaximized()
        self.menu = ScreenMenu()
        self.menu.setGameConfig(self.gameconfig)
        self.menu.setUpLevel(self.level)
        self.controller.setScreenMenu(self.menu)
        self.scene.addItem(self.controller.cursor)
        self.menu.setUpGui(self.view)
        self.menu.setScene(self.scene)



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
        sys.exit(app.exec_())

if __name__ == '__main__':
    from mechanics.AI.SimGame import SimGame as DreamGame
    from content.base_types.demo_hero import demohero_basetype
    from content.dungeons.demo_dungeon import demo_dungeon
    from game_objects.battlefield_objects import Unit

    from threading import Thread



    game = DreamGame.start_dungeon(demo_dungeon, Unit(demohero_basetype))
    Thread(target=game.loop).start()

    app = QtWidgets.QApplication(sys.argv)
    window = TheUI(game)
    sys.exit(app.exec_())
