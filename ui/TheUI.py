import sys

from PySide2 import QtCore, QtGui, QtWidgets

from ui.menu import ScreenMenu
from ui.gamecontroller import GameController
from ui.levels import Level_demo_dungeon

from ui.GameView import GameView


class TheUI(QtWidgets.QWidget):
    view = None
    def __init__(self, game):

        super().__init__()
        self.the_game = game
        self.gameTimer = QtCore.QTimer()
        self.gameTimer.timeout.connect(self.timerSlot)
        self.gameTimer.startTimer(int(1000 / 50))

        cursor = QtGui.QCursor(QtGui.QPixmap('resources/assets/ui/cursor.png'))
        self.setCursor(cursor)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.view = GameView(self)
        self.gameconfig = self.view.gameconfig
        self.layout.addWidget(self.view)
        self.layout.setMargin(2)

        self.scene = QtWidgets.QGraphicsScene(0, 0, 500, 500)
        self.scene.setFocus(focusReason=QtCore.Qt.OtherFocusReason)
        self.scene.setBackgroundBrush(QtGui.QBrush(self.gameconfig.getPicFile('dungeon.jpg')))


        menu = ScreenMenu()
        self.controller = GameController(self.gameconfig, self.the_game, self.view, self.scene, menu)

        self.level = Level_demo_dungeon(self.gameconfig)
        self.level.setUpLevel(self.the_game, self.controller)

        self.scene.addItem(self.level.world)
        self.scene.addItem(self.level.units)
        self.scene.addItem(self.level.middleLayer)
        self.scene.addItem(self.controller.cursor)

        self.view.resized.connect(menu.updateGui)
        menu.setGameConfig(self.gameconfig)
        menu.setUpLevel(self.level)
        menu.setUpGui(self.view)
        menu.setScene(self.scene)


        self.view.controller = self.controller
        self.view.setScene(self.scene)

        self.showMaximized()



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
