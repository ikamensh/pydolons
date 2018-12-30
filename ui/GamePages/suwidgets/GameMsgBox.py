from PySide2 import QtCore, QtWidgets


class GameMsgBox(QtWidgets.QDialog):

    OK = 0
    CANCEL = 1
    SAVE = 2

    def __init__(self, parent = None):
        super(GameMsgBox, self).__init__(parent)
        self.setStyleSheet("background-image: url('resources/UI/Assets/scroll_background.png');")
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setFixedSize(640, 480)
        self.finished.connect(self.hide)
        self.setUpWigets()

    def setGameConfig(self, cfg):
        if cfg.dev_size[0] < 1439:
            w = 640
        elif cfg.dev_size[0] < 1919:
            w = 780
        elif cfg.dev_size[0] >= 1920:
            w = 1120
        if cfg.dev_size[1] < 800:
            h = 480
        elif cfg.dev_size[1] < 1050:
            h = 640
        elif cfg.dev_size[1] >= 1050:
            h = 960
        self.setFixedSize(w, h)

    def setUpWigets(self):
        self.grid = QtWidgets.QGridLayout(self)
        self.tetx_label = QtWidgets.QLabel('text')
        self.grid.addWidget(self.tetx_label, 1, 0, alignment = QtCore.Qt.AlignCenter)
        self.info_text_label = QtWidgets.QLabel('info text')
        self.grid.addWidget(self.info_text_label, 2, 0, 3, 1, alignment = QtCore.Qt.AlignCenter)
        self.btn_layout = QtWidgets.QHBoxLayout()
        but = self.getButton('Ok')
        but.clicked.connect(self.accept)
        self.btn_layout.addWidget(but)
        self.grid.addLayout(self.btn_layout, 7, 0, alignment = QtCore.Qt.AlignRight)

    def setInformativeText(self, text, format = QtCore.Qt.AutoText):
        self.info_text_label.setTextFormat(format)
        self.info_text_label.setText(text)
        pass

    def setText(self, text, format = QtCore.Qt.AutoText):
        self.tetx_label.setTextFormat(format)
        self.tetx_label.setText(text)
        pass

    # def setDefaultButton(self, button):
    #     pass

    def setStandardButtons(self, *args):
        if args != ():
            self.btn_layout = QtWidgets.QHBoxLayout()
            for index in args:
                if index == 0:
                    but = self.getButton('Ok')
                    but.clicked.connect(self.accept)
                    self.btn_layout.addWidget(but)
                elif index == 1:
                    but = self.getButton('Cancel')
                    but.clicked.connect(self.reject)
                    self.btn_layout.addWidget(but)
                elif index == 2:
                    self.btn_layout.addWidget(self.getButton('Save'))
        self.grid.addLayout(self.btn_layout, 7, 0, alignment=QtCore.Qt.AlignRight)
        pass

    def getButton(self, name):
        button = QtWidgets.QPushButton(name, self)
        return button

    def accept(self):
        self.accepted.emit()
        self.finished.emit(0)
        self.setResult(0)

    def reject(self):
        self.rejected.emit()
        self.finished.emit(1)
        self.setResult(1)
