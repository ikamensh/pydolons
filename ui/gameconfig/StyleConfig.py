from PySide2.QtGui import QColor, QBrush


class StyleConfig:
    def __init__(self):
        self.colors = {}
        self.brushs = {}
        self.setUpColors()

    def setUpColors(self):
        self.colors['b5adb7'] = QColor('#b5adb7')
        self.brushs['b5adb7'] = QBrush(self.colors['b5adb7'])
        self.colors['ff6600'] = QColor('#ff6600')
        self.brushs['ff6600'] = QBrush(self.colors['ff6600'])
        self.colors['d7a784'] = QColor('#d7a784')
        self.brushs['d7a784'] = QBrush(self.colors['d7a784'])
