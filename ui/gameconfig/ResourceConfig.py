from PySide2.QtGui import QPixmap, QFont, QFontDatabase

from PySide2.QtMultimedia import QSound

from config import pydolons_rootdir
from mechanics.damage import DamageTypes
from ui.gameconfig.GameSizeConfig import gameItemsSizes

import os
from datetime import datetime
from xml.etree import ElementTree as ET


class ResourceConfig:
    def __init__(self, cfg, lazy = True):
        self.ignore_path = ('resources/assets/sprites/axe',)  # Игнорируемые папки
        self.rez_step = 0
        self.pic_formats = ('png', 'jpg')
        self.pic_file_paths = {}
        self.pix_maps = {}

        self.sound_formats = ('wav', 'mp3')
        self.sound_file_paths = {}
        self.sound_maps = {}

        self.fonts_formats = ('ttf')
        self.fonts_file_paths = {}
        self.fonts_maps = {}

        self.xml_file_paths = {}
        self.xml_maps = {}

        self.setUpUnits()
        self.loadFilesPath()
        print('cfg ===> loadFilesPath', datetime.now())
        self.lazy = lazy
        if lazy:
            self.setUpPixmaps()
            print('cfg ===> setUpPixmaps', datetime.now())
        self.setUpSounds()
        self.setUpFonts()
        self.setUpXML_Page()

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
                    elif name[-3:].lower() in self.fonts_formats:
                        self.fonts_file_paths[name.lower()] = os.path.join(item[0], name)
                    elif name[-3:] == 'xml':
                        self.xml_file_paths[name] = os.path.join(item[0], name)

    #### P I X M A P ####

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
                pixmap = QPixmap(path)
                self.pix_maps[filename] = pixmap
            except Exception as e:
                print(e)

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
            size = self.getSize(id)
            pixmap = pixmap.scaled(size[0], size[1])
        return pixmap

    def getSize(self, id):
        size = gameItemsSizes.get(id)
        if size is None:
            print("d'ont get size for id, set default")
            return (64, 64)
        else:
            return size[self.rez_step]

    #### S O U N D S ####

    def setUpSounds(self):
        for filename, path in self.sound_file_paths.items():
            sound = None
            try:
                sound = QSound(path)
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

    #### F O N T S ####

    def setUpFonts(self):
        for filename, path in self.fonts_file_paths.items():
            font = None
            try:
                id = QFontDatabase.addApplicationFont(path)
                name = QFontDatabase.applicationFontFamilies(id)[0]
                font = QFont(name)
                self.fonts_maps[filename] = font
                self.main_font_name = name
            except Exception as e:
                print(e)

    #### X M L  P A G E ####

    def setUpXML_Page(self):
        for filename, xml_path in self.xml_file_paths.items():
            self.xml_maps[filename] = ET.parse(xml_path)

    def getXML_Page(self, name):
        page = self.xml_maps.get(name)
        if page is not None:
            return page
        else:
            return self.xml_maps.get('404_page.xml')

