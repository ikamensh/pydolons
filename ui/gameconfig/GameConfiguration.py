from ui.gameconfig.UserConfig import UserConfig, DEFAULT_CONFIG
from ui.gameconfig.DeviceConfig import DeviceConfig
from ui.gameconfig.ResourceConfig import ResourceConfig
from ui.gameconfig.StyleConfig import StyleConfig

from datetime import datetime
from copy import copy


class GameConfiguration:
    """docstring for GameConfiguration.
    Установка основных конфигураций игры
    """
    def __init__(self, lazy = True):
        print('cfg ===> start init', datetime.now())

        self.deviceConfig = None
        self.userConfig = None
        self.resourceConfig = None
        self.styleConfig = None

        # Setup configuration for curent device
        self.deviceConfig = DeviceConfig(self)
        # Setup configuration from user config file
        self.setUpUserConfig()
        # Setup size steps
        self.rez_step = self.getStep()
        # Setup configuration from resources
        self.setUpResourceConfig(lazy)
        # Setup configuration from styles
        self.setUpStyleConfig()
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

    def setUpResourceConfig(self, lazy):
        """from Resource Config"""
        self.resourceConfig = ResourceConfig(lazy)
        self.resourceConfig.rez_step =self.rez_step
        self.pix_maps = self.resourceConfig.pix_maps
        self.unit_size = self.resourceConfig.unit_size
        self.pic_file_paths = self.resourceConfig.pic_file_paths
        self.sound_maps = self.resourceConfig.sound_maps

    def getSize(self, id):
        """from Resource Config"""
        return self.resourceConfig.getSize(id)

    def getPicFile(self, filename, id = None, size = None):
        """from Resource Config"""
        return self.resourceConfig.getPicFile(filename, id, size)

    def setUpUserConfig(self):
        """from User Config"""
        self.userConfig = UserConfig()
        try:
            self.userConfig.readSetting()
        except Exception as e:
            self.userConfig.read_config = copy(DEFAULT_CONFIG)
        finally:
            if self.userConfig.read_config['window']['resolution'] != 'current':
                self.dev_size = self.userConfig.read_config['window']['resolution']['width'],\
                        self.userConfig.read_config['window']['resolution']['height']

    @property
    def dev_cfg_size(self):
        """from User Config"""
        print(self.userConfig.read_config)
        if not self.userConfig.read_config['window']['fullscreen']:
            return self.userConfig.read_config['window']['resolution']['width'], \
                   self.userConfig.read_config['window']['resolution']['height']

    def setUpStyleConfig(self):
        self.styleConfig = StyleConfig()
        self.colors = self.styleConfig.colors
        self.brushs = self.styleConfig.brushs

    def getStep(self):
        if self.dev_size[1] < 900:
            return 0
        elif self.dev_size[1] > 1079:
            return 2
        else:
            return 1













