from __future__ import annotations
from PySide2.QtGui import QColor, QBrush, QFont, QFontInfo, QFontDatabase, QGuiApplication
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.gamecore.gameconfig.GameConfiguration import GameConfiguration

class StyleConfig:
    def __init__(self, cfg: GameConfiguration):
        self.colors = {}
        self.brushs = {}
        self.setUpColors()
        self.cfg = cfg
        self.system_font :QFont = QGuiApplication.font()
        self.system_hint = self.system_font.hintingPreference()
        self.system_pixelSize = self.system_font.pixelSize()
        self.default_pixel_size = 15
        self.default_point_size = 16
        self.default_weight = 50
        self.setUpFonts()

    def setUpColors(self):
        self.colors['b5adb7'] = QColor('#b5adb7')
        self.brushs['b5adb7'] = QBrush(self.colors['b5adb7'])
        self.colors['ff6600'] = QColor('#ff6600')
        self.brushs['ff6600'] = QBrush(self.colors['ff6600'])
        self.colors['d7a784'] = QColor('#d7a784')
        self.brushs['d7a784'] = QBrush(self.colors['d7a784'])

    def setUpFonts(self):
        info = QFontInfo(self.system_font)
        print('pixel_size', info.pixelSize())
        print('point_size', info.pointSize())
        print('point_size_f', info.pointSizeF())
        print('weight', info.weight())
        print('styleHint', info.styleHint())

        self.main_font:QFont = self.cfg.resourceConfig.fonts_maps['imfeenrm28p.ttf']
        self.base_point_size = int(self.default_point_size * self.cfg.scale_y)
        self.base_pixel_size = int(self.default_pixel_size * self.cfg.scale_y)
        self.base_weight = int(self.default_weight * self.cfg.scale_y)
        self.main_font.setPixelSize(self.base_pixel_size)
        self.main_font.setPointSize(self.base_point_size)
        self.main_font.setWeight(self.default_weight)
        QGuiApplication.setFont(self.main_font)

    def calculateScales(self):
        WIDTH = 1920
        HEIGHT = 1080
        self.scale_x = self.cfg.dev_size[0] / WIDTH
        self.scale_y = self.cfg.dev_size[1] / HEIGHT
        print('scales x:y = ', self.scale_x, self.scale_y)
        print('font system_hint', self.system_hint)
        print('font system_pixelSize', self.system_pixelSize)

    def getFont(self, name = None):
        # print(self.cfg.resourceConfig.main_font_name)
        font = None
        if name is None:
            name = 'IM FELL English'
        __ = self.cfg.resourceConfig.fonts_maps.get(name)
        if __ is None:
            font = QFont('IM FELL English')
        else:
            font = QFont(name)
        font.setPointSize(self.base_point_size)
        font.setPixelSize(self.default_pixel_size)
        font.setWeight(self.default_weight)
        return font
