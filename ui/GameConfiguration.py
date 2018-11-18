import os
from PySide2 import QtGui, QtWidgets, QtMultimedia
from ui.GameSizeConfig import gameItemsSizes

from config import pydolons_rootdir
from mechanics.damage import DamageTypes

from datetime import datetime

class GameConfiguration:
    """docstring for GameConfiguration.
    Установка конфигурации игровых объектов, настроек экрана и системы
    """
    def __init__(self, lazy = True):
        print('cfg ===> start init', datetime.now())
        self.ignore_path = ('resources/assets/sprites/axe', )         # Игнорируемые папки


        self.pic_formats = ('png', 'jpg')
        self.pic_file_paths = {}
        self.pix_maps = {}


        self.sound_formats = ('wav', 'mp3')
        self.sound_file_paths = {}
        self.sound_maps = {}

        self.setUpScreen()
        print('cfg ===> setUpScreen', datetime.now())
        self.setUpUnits()
        self.loadFilesPath()
        print('cfg ===> loadFilesPath', datetime.now())
        self.lazy = lazy
        if lazy:
            self.setUpPixmaps()
            print('cfg ===> setUpPixmaps', datetime.now())
        self.setUpSounds()
        print('cfg ===> setUpSounds', datetime.now())
        self.gameRoot = None
        self.tr = QtGui.QTransform()

    def setGameRoot(self, gameRoot):
        self.gameRoot =  gameRoot
        self.gameRoot.cfg = self

    def setWorld(self, world):
        """
        метод добавляет атрибуты игрового мира, которые доступны все классам
        """
        self.world_size = world.worldSize
        self.world_a_size = world.worldHalfSize


    def setUpScreen(self):
        """
        :atribute ava_size  - доступный размер
        :atribute dev_size  - размер устройства
        :atribute ava_ha_size  - доступный размер деленый на 2
        :atribute dev_size  - размер устройства деленый на 2
        """
        self.desktop =  QtWidgets.QDesktopWidget()
        self.dev_size = self.desktop.screenGeometry().width(), self.desktop.screenGeometry().height()
        if self.dev_size[1] < 900:
            self.rez_step = 0
        else:
            self.rez_step = 1
            if self.dev_size[1] > 1079:
                self.rez_step = 2
        self.dev_ha_size = int(self.dev_size[0] / 2), int(self.dev_size[1] / 2)
        self.ava_size = self.desktop.availableGeometry().width(), self.desktop.availableGeometry().height()
        self.ava_ha_size = int(self.ava_size[0] / 2), int(self.ava_size[1] / 2)
        self.correct_size = self.ava_ha_size[0] - 3, self.ava_ha_size[1] - 17

    def updateScreenSize(self, w, h):
        self.screenSize = (w, h)
        self.dev_size = self.screenSize
        self.tr.reset()
        self.tr.translate(w/2, h/2)

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
        self.walks = os.walk(top = os.path.join(pydolons_rootdir, 'resources') )
        # Словарь путей к изображениям, ключ название файла
        # self.pic_file_paths = {}
        # получаем данные генератора
        for item in self.walks:
            # если список файлов пуст и путь не находится среди игнорируемых
            if item[2] != [] and not item[0] in self.ignore_path:
                # Получаем спискок фйалов
                for name in item[2]:
                    if name[-3:].lower() in self.pic_formats:
                        self.pic_file_paths[name.lower()] = os.path.join(item[0], name)
                    elif name[-3:].lower() in self.sound_formats:
                        self.sound_file_paths[name.lower()] = os.path.join(item[0], name)


    def getPicFile(self, filename, id = None, size = None):
        """
        если файл не найден генерируется ошибка
        argument: filename -- название файла в файловой системе
        return: QtGui.QPixmap
        Объект QPixmap из словаря GameConfiguration.pix_maps
        """
        filename = filename.lower()
        pixmap = self.pix_maps.get(filename)
        if pixmap is None:
            # print(filename + ' image was not found. using default.')
            pixmap = self.pix_maps.get("default_128.png")
        if not id is None:
            size = gameItemsSizes.get(id)
            if not size is None:
                pixmap = pixmap.scaled(size[self.rez_step][0], size[self.rez_step][1])
        return pixmap

    def setUpSounds(self):
        for filename, path in self.sound_file_paths.items():
            sound = None
            try:
                # print('load ', filename)
                sound = QtMultimedia.QSound(path)
                self.sound_maps[filename] = sound
            except Exception as e:
                print(filename, ' : ', e)
        # set Up from damage type
        self.sound_maps[DamageTypes.CRUSH] = self.sound_maps['bash.wav']
        self.sound_maps[DamageTypes.SLASH] = self.sound_maps['slash.wav']
        self.sound_maps[DamageTypes.PIERCE] = self.sound_maps['pierce.wav']
        self.sound_maps[DamageTypes.FIRE] = self.sound_maps['fire.wav']
        # self.sound_maps[DamageTypes.ICE] = self.sound_maps['ice.wav']
        self.sound_maps[DamageTypes.LIGHTNING] = self.sound_maps['lightning.wav']
        self.sound_maps[DamageTypes.ACID] = self.sound_maps['acid.wav']
        # self.sound_maps[DamageTypes.SONIC] = self.sound_maps['soinc.wav']

    def setUpPixmaps(self):
        """Метод перебирает словарь GameConfiguration.pic_file_paths
        получает название файла, путь к файлу. Формирует объект QtGui.QPixmap
        которы добавляется в словарь GameConfiguration.pix_maps
        {filename: QtGui.QPixmap()}
        """
        if self.lazy:
            print('lazy')
        for filename, path in self.pic_file_paths.items():
            pixmap = None
            try:
                pixmap = QtGui.QPixmap(path)
                self.pix_maps[filename] = pixmap
            except Exception as e:
                print(e)



