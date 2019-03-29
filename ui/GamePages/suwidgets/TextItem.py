from PySide2.QtWidgets import QGraphicsSimpleTextItem
from PySide2.QtGui import QFont, QColor, QBrush
from PySide2 import QtCore


class TextItem(QGraphicsSimpleTextItem):
    def __init__(self, page, parent=None):
        super(TextItem, self).__init__(parent)
        self.gameRoot = page.gamePages.gameRoot
        self.page = page
        self.attrib = None
        self.cfg = page.gamePages.gameRoot.cfg
        self.scale_x = self.gameRoot.cfg.scale_x
        self.scale_y = self.gameRoot.cfg.scale_y

    def setUpAttrib(self, attrib):
        """
        :param attrib:
        :return:


        top = '128'
        background - color = "000000"
        color = "FF0000"
        icon = "default.png"
        type = "other"

        """
        self.attrib = attrib
        self.checkAttrib(attrib)
        self.name = attrib['name']
        self._names = attrib['name'].split('_')
        self._top = int(attrib.get('top')) * self.scale_y
        self._left = int(attrib.get('left')) * self.scale_x
        self._width = int(attrib.get('width')) * self.scale_x
        self._height = int(attrib.get('height')) * self.scale_x
        if attrib.get('position') is not None:
            self._position = attrib.get('position')
            if self._position == 'inherit':
                if self._parent_node is not None:
                    self._top = self.page.items[self._parent_node]._top + self._top
                    self._left = self.page.items[self._parent_node]._left + self._left
        # self.pixmap = self.gameRoot.cfg.getPicFile(attrib['icon'])
        self.setPos(self._left, self._top)
        self.setUpTextOptions(attrib)
        self._color = attrib['color']
        brush = QBrush(QColor(attrib['color']))
        self.setBrush(brush)
        pass

    # def checkAttrib(self, attrib):
    #     if attrib.get('top') is None:
    #         attrib['top'] = 1080 - int(attrib['bottom'])
    #     if attrib.get('left') is None:
    #         attrib['left'] = 1920 - int(attrib['right'])
    #     self._parent_node = attrib.get('parent_node')

    def checkAttrib(self, attrib):
        if attrib.get('width') is None:
            attrib['width'] = '0'
        if attrib.get('height') is None:
            attrib['height'] = '0'
        if attrib.get('top') is None:
            attrib['top'] = 1080 - int(attrib['bottom'])
        if attrib.get('left') is None:
            attrib['left'] = 1920 - int(attrib['right'])
        self._parent_node = attrib.get('parent_node')

        if attrib.get('background-color') is not None:
            self._bg_brush = QBrush(QColor(attrib['background-color']))
        if attrib.get('color') is None:
            attrib['color'] = '#FFFFFF'
        if attrib.get('icon') is not None:
            self.pixmap = self.gameRoot.cfg.getPicFile(attrib['icon'])
        if attrib.get('background-color') is not None:
            self.paint = self.paint_bg
        if attrib.get('icon') is not None:
            self.paint = self.paint_pic
        if attrib.get('icon') is not None and attrib.get(
                'background-color') is not None:
            self.paint = self.paint_pic_bg
        if attrib.get('input') is None:
            self.input = ''
        else:
            self.input = attrib.get('input')

    def setUpTextOptions(self, attrib):
        # self.setPlainText(attrib['text'])
        self.setText(attrib['text'])
        self._font = QFont(self.cfg.main_font_name)
        self._font.setPointSize(
            int(self.cfg.styleConfig.base_point_size * self.scale_x))
        if attrib.get('font_size') is not None:
            self._font.setPointSize(
                int(attrib.get('font_size')) * self.scale_x)
        self.setFont(self._font)
        # if self.document().size().width() > self._width:
        #     while self.document().size().width() > self._width:
        #         self._font = QFont(self.cfg.main_font_name)
        #         self._font.setPointSize(self.font().pointSize() - 1)
        #         self.setFont(self._font)

    def setColor(self, color):
        self.setBrush(QBrush(QColor(color)))
