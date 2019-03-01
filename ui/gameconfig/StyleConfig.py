from PySide2.QtGui import QColor, QBrush, QFont, QFontDatabase, QGuiApplication


class StyleConfig:
    def __init__(self, cfg):
        self.colors = {}
        self.brushs = {}
        self.setUpColors()
        self.cfg = cfg
        self.system_font :QFont = QGuiApplication.font()
        self.system_hint = self.system_font.hintingPreference()
        self.system_pixelSize = self.system_font.pixelSize()
        self.setUpFonts()

    def setUpColors(self):
        self.colors['b5adb7'] = QColor('#b5adb7')
        self.brushs['b5adb7'] = QBrush(self.colors['b5adb7'])
        self.colors['ff6600'] = QColor('#ff6600')
        self.brushs['ff6600'] = QBrush(self.colors['ff6600'])
        self.colors['d7a784'] = QColor('#d7a784')
        self.brushs['d7a784'] = QBrush(self.colors['d7a784'])

    def setUpFonts(self):
        self.main_font = self.cfg.resourceConfig.fonts_maps['imfeenrm28p.ttf']
        pointSize = int(self.system_font.pointSize()*self.cfg.scale_x)
        self.main_font.setPointSize(pointSize)
        # self.main_font.set
        QGuiApplication.setFont(self.main_font)
