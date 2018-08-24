import sys
import math
from os import path, walk
#
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Slot
#
from menu import ScreenMenu
from units import Units
from gameutils import GameMath
from gamecontroller import GameController
from levels import *
from units import GameObject
#
from DreamGame import DreamGame
from content.base_types.demo_hero import demohero_basetype
from content.dungeons.demo_dungeon import demo_dungeon
from game_objects.battlefield_objects import Unit
from mechanics.events import MovementEvent
from GameLog import gamelog
from battlefield.Battlefield import Battlefield, Cell
from content.actives.std_melee_attack import attack_cell_active, attack_unit_active
#

class GameConfiguration(object):
    """docstring for GameConfiguration.
    Установка конфигурации игровых объектов, настроек экрана и системы
    """
    def __init__(self):
        """
        Форматы изображений
        pic_format = ('png', )
        Игнорируемые папки
        ignore_path = (dirpath, )
        Словарь путей к изображениям, ключ название файла
        pic_file_paths = {}
        """
        super(GameConfiguration, self).__init__()
        # Форматы изображений
        self.pic_format = ('png', 'jpg')
        # Игнорируемые папки
        self.ignore_path = ('resources/assets/sprites/axe', )
        # Словарь путей к изображениям, ключ название файла
        self.pic_file_paths = {}

        self.setUpScreen()
        self.setUpUnits()
        self.loadFilesPath()
        self.setUpPixmaps()

    def setWorld(self, world):
        """
        метод добавляет атрибуты игрового мира, которые доступны все классам
        self.world_size = world.worldSize
        self.world_a_size = world.worldHalfSize
        """
        self.world_size = world.worldSize
        self.world_a_size = world.worldHalfSize

    def setUpLevel(self, world = None):
        """временный метод, аргументы будут расширены позже
        """
        if world:
            self.setWorld(world)

    def setUpScreen(self):
        """
        :atribute ava_size  - доступный размер
        :atribute dev_size  - размер устройства
        :atribute ava_ha_size  - доступный размер деленый на 2
        :atribute dev_size  - размер устройства деленый на 2
        """
        self.desktop =  QtWidgets.QDesktopWidget()
        self.dev_size = self.desktop.screenGeometry().width(), self.desktop.screenGeometry().height()
        self.dev_ha_size = int(self.dev_size[0] / 2), int(self.dev_size[1] / 2)
        self.ava_size = self.desktop.availableGeometry().width(), self.desktop.availableGeometry().height()
        self.ava_ha_size = int(self.ava_size[0] / 2), int(self.ava_size[1] / 2)
        self.correct_size = self.ava_ha_size[0] - 3, self.ava_ha_size[1] - 17

    def setUpUnits(self):
        """
        :atribute unit_size  - максимальный размер юнита
        :atribute unit_x_size -  размер юнита c умноженный на x, где  x = [a = 1/2, b = 1/3, c = 1/4]
        """
        self.unit_size = 128, 128
        self.unit_a_size = int(self.unit_size[0] * (1/2)), int(self.unit_size[0] * (1/2))
        self.unit_b_size = int(self.unit_size[0] * (1/3)), int(self.unit_size[0] * (1/3))
        self.unit_c_size = int(self.unit_size[0] * (1/4)), int(self.unit_size[0] * (1/4))

    def loadFilesPath(self):
        """
        метод сканирует файловую систему, если в папке resources
        есть файл то пути к файлам будут добавлены в словарь GameConfiguration.pic_file_paths
        Словарь вида {filename: filepath}
        """
        # генератор путей, файлов и папок
        self.walks = walk(top = 'resources')
        # Словарь путей к изображениям, ключ название файла
        # self.pic_file_paths = {}
        # получаем данные генератора
        for item in self.walks:
            # если список файлов пуст и путь не находится среди игнорируемых
            if item[2] != [] and not item[0] in self.ignore_path:
                # print(item[0])
                # Получаем спискок фйалов
                for name in item[2]:
                    # Если расширение файла совпадает с форматом
                    if name[-3:] in self.pic_format:
                        # Добавляем в словарь
                        self.pic_file_paths[name] = path.join(item[0], name)

    def getPicFile(self, filename):
        """
        если файл не найден генерируется ошибка
        argument: filename -- название файла в файловой системе
        return: QtGui.QPixmap
        Объект QPixmap из словаря GameConfiguration.pix_maps
        """
        assert not self.pix_maps.get(filename) is None
        return self.pix_maps.get(filename)

    def setUpPixmaps(self):
        """Метод перебирает словарь GameConfiguration.pic_file_paths
        получает название файла, путь к файлу. Формирует объект QtGui.QPixmap
        которы добавляется в словарь GameConfiguration.pix_maps
        {filename: QtGui.QPixmap()}
        """
        self.pix_maps = {}
        for filename, path in self.pic_file_paths.items():
            pixmap = None
            try:
                pixmap = QtGui.QPixmap(path)
                self.pix_maps[filename] = pixmap
            except Exception as e:
                print(e)



class MyView(QtWidgets.QGraphicsView):
    def __init__(self, parent = None):
        QtWidgets.QGraphicsView.__init__(self, parent)
        self.setMouseTracking(True)

        self.item = SelectItem(0, 0, 32, 32)
        self.controller = None

    def wheelEvent(self, e):
        self.controller.wheelEvent(e)


    def keyPressEvent(self, e):
        self.controller.keyPressEvent(e)

    def mouseMoveEvent(self, e):
        self.controller.mouseMoveEvent(e)

    def mousePressEvent(self, e):
        self.controller.mousePressEvent(e)

class GameManager(object):
    """docstring for GameManager."""
    def __init__(self):
        super(GameManager, self).__init__()

    def setUp(self, controller):
        # self.level = level
        self.controller = controller
        self.dun_game = DreamGame.start_dungeon(demo_dungeon, Unit(demohero_basetype))
        self.setActiveUnit()

    def setActiveUnit(self):
        if not self.dun_game.game_over():
            self.dun_game.active_unit = self.dun_game.turns_manager.get_next()

    def getActiveUnit(self):
        return self.dun_game.active_unit

    def getUnitFacings(self):
        return self.dun_game.battlefield.unit_facings

    def moveHero(self, point):
        target_location = Cell(point[0] + 4, point[1] + 4)
        self.dun_game.order_move(self.dun_game.the_hero, target_location)

    def attackHero(self, point):
        target_location = Cell(point[0] + 4, point[1] + 4)
        active_cpy = self.dun_game.the_hero.give_active(attack_cell_active)
        self.dun_game.the_hero.activate(active_cpy, target_location)

    def setFacingHero(self, facing):
        self.dun_game.battlefield.unit_facings[self.dun_game.the_hero] = facing

    def nextStep(self):
        if not self.dun_game.game_over():
            # print(self.dun_game.turns_manager.managed)
            active, target = self.dun_game.brute_ai.decide_step(self.dun_game.active_unit)
            self.dun_game.active_unit.activate(active, target)
            self.dun_game.game_over()
        else:
            print('end game')



class Window(QtWidgets.QWidget):
    """docstring for Window."""
    view = None
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
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

        self.controller = GameController(self.gameconfig)
        self.controller.setView(self.view)
        self.controller.scene = self.scene
        self.gameManager = GameManager()
        self.gameManager.setUp(self.controller)

        self.level = Level_demo_dungeon(self.gameconfig)
        self.level.setController(self.controller)
        self.level.setUpLevel(self.gameManager.dun_game)
        self.controller.setManager(self.gameManager)
        self.scene.addItem(self.level.world)
        self.scene.addItem(self.level.units)
        self.scene.addItem(self.level.midleLayer)
        # self.itemBGR.setOffset(self.pixBGR.size().width()/-2, self.pixBGR.size().height()/-2)
        # self.view.mymap = self.itemBGR
        # self.scene.addItem(self.itemBGR)
        # self.units = Units()
        # self.scene.addItem(self.units)
        # self.view.units = self.units
        # self.controller.setHero(self.units.hero)
        self.view.controller = self.controller
        # self.showFullScreen()
        self.showMaximized()
        self.menu = ScreenMenu()
        self.menu.setGameConfig(self.gameconfig)
        self.menu.setUpLevel(self.level)
        self.controller.setScreenMenu(self.menu)
        self.scene.addItem(self.controller.cursor)
        self.menu.setUpGui(self.view)
        self.menu.setScene(self.scene)

        # self.log_plain.widget().setFocusProxy(self.view)
        # self.view.setFocusProxy(self.log_plain.widget())
        # self.log_plain.pos().setX(128)
        # self.log_plain.pos().setY(256)
        # print('self.log_plain.pos = ',self.log_plain.pos())
        # print('self.log_plain dir :\n',dir(self.log_plain))
        # self.scene.changed.connect(self.changeTo)


    def changeTo(self):
        self.scene.update(-self.gameconfig.ava_ha_size[0],
                          -self.gameconfig.ava_ha_size[1],
                          self.gameconfig.ava_size[0],
                          self.gameconfig.ava_size[1])

    def timerSlot(self):
        print('timerSlot')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    # QtCore.QObject.connect(window.btn_quit, QtCore.SIGNAL("clicked()"),
    #                        app, QtCore.SLOT("quit()"))
    sys.exit(app.exec_())
