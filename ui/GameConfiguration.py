import os
from PySide2 import QtGui, QtWidgets, QtMultimedia

from my_context import pydolons_rootdir

class GameConfiguration:
    """docstring for GameConfiguration.
    Установка конфигурации игровых объектов, настроек экрана и системы
    """
    def __init__(self):
        # Игнорируемые папки
        self.ignore_path = ('resources/assets/sprites/axe', )
        # Форматы изображений
        self.pic_format = ('png', 'jpg')
        # Словарь путей к изображениям, ключ название файла
        self.pic_file_paths = {}
        # Форматы звуков
        self.sound_format = ('wav')
        # Словарь путей к звукам, ключ название файла
        self.sound_file_paths = {}
        self.setUpScreen()
        self.setUpUnits()
        self.loadFilesPath()
        self.setUpPixmaps()
        self.setUpSounds()
        self.gameRoot = None

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
        self.dev_ha_size = int(self.dev_size[0] / 2), int(self.dev_size[1] / 2)
        self.ava_size = self.desktop.availableGeometry().width(), self.desktop.availableGeometry().height()
        self.ava_ha_size = int(self.ava_size[0] / 2), int(self.ava_size[1] / 2)
        self.correct_size = self.ava_ha_size[0] - 3, self.ava_ha_size[1] - 17

    def updateScreenSize(self, w, h):
        self.screenSize = (w, h)
        self.dev_size = self.screenSize

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
                    if name[-3:] in self.pic_format:
                        self.pic_file_paths[name] = os.path.join(item[0], name)
                    elif name[-3:] in self.sound_format:
                        self.sound_file_paths[name] = os.path.join(item[0], name)

    def getPicFile(self, filename):
        """
        если файл не найден генерируется ошибка
        argument: filename -- название файла в файловой системе
        return: QtGui.QPixmap
        Объект QPixmap из словаря GameConfiguration.pix_maps
        """
        assert self.pix_maps.get(filename) is not None
        return self.pix_maps.get(filename)

    def setUpSounds(self):
        self.sound_maps = {}
        for filename, path in self.sound_file_paths.items():
            sound = None
            try:
                sound = QtMultimedia.QSound(path)
                self.sound_maps[filename] = sound
            except Exception as e:
                print(filename, ' : ', e)

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
