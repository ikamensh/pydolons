

class GroupItem:
    def __init__(self, page, parent=None):
        self.gameRoot = page.gamePages.gameRoot
        self.page = page
        self.attrib = None
        self.cfg = page.gamePages.gameRoot.cfg
        self.scale_x = self.gameRoot.cfg.scale_x
        self.scale_y = self.gameRoot.cfg.scale_y
        self.scale_x = self.scale_y
        self.pixmap = None
        self._bg_brush = None

    def setUpAttrib(self, attrib):
        self.attrib = attrib
        self.checkAttrib(attrib)
        self.name = attrib['name']
        self._top = int(attrib.get('top')) * self.scale_x
        self._left = int(attrib.get('left')) * self.scale_x
        self._width = int(attrib.get('width')) * self.scale_x
        self._height = int(attrib.get('height')) * self.scale_x
        if attrib.get('position') is not None:
            self._position = attrib.get('position')
            if self._position == 'inherit':
                if self._parent_node is not None:
                    self._top = self.page.items[self._parent_node]._top + self._top
                    self._left = self.page.items[self._parent_node]._left + self._left

        pass

    def checkAttrib(self, attrib):
        if attrib.get('top') is None:
            attrib['top'] = 1080 - int(attrib['bottom'])
        if attrib.get('left') is None:
            attrib['left'] = 1920 - int(attrib['right'])
        self._parent_node = attrib.get('parent_node')
        if attrib.get('icon') is not None:
            self.pixmap = self.gameRoot.cfg.getPicFile(attrib['icon'])
        if attrib.get('background-color') is not None:
            self.paint = self.paint_bg
        if attrib.get('icon') is not None:
            self.paint = self.paint_pic
        if attrib.get('icon') is not None and attrib.get('background-color') is not None:
            self.paint = self.paint_pic_bg
