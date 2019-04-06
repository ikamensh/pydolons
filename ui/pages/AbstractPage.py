from __future__ import annotations

from abc import ABC, abstractmethod
from PySide2 import QtWidgets, QtCore
from ui.pages.suwidgets.BaseItem import BaseItem
from ui.pages.suwidgets.TextItem import TextItem
from ui.pages.suwidgets.GroupItem import GroupItem
from xml.etree import ElementTree as ET
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.pages import GamePages


class AbstractPage(QtCore.QObject, QtWidgets.QGraphicsItemGroup):
    """docstring for AbstractPage."""
    focusable = QtCore.Signal(bool)
    ITEM_TYPES = {'other':BaseItem, 'text':TextItem, 'group':GroupItem}

    def __init__(self, gamePages, parent = None):
        QtCore.QObject.__init__(self, parent)
        QtWidgets.QGraphicsItemGroup.__init__(self)
        self.xml_page = None
        self.items = {}
        self.widget_pos = QtCore.QPoint()
        self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations, True)
        self.gamePages: GamePages = gamePages
        self.mainWidget: QtWidgets.QGraphicsWidget = None
        self.state = False
        self.isService = False

    def read_tree(self, start_node = None):
        if start_node is None:
            start_node = self.xml_page
        visited = {}  # изначально список посещённых узлов пуст
        for node in start_node.iter():
            visited[node] = False
        queue = list()
        queue.append(start_node)  # начиная с узла-источника
        visited[start_node] = True
        while len(queue) != 0:  # пока очередь не пуста
            node = queue.pop()  # извлечь первый элемент в очереди
            self.create_item(node)
            # if node == goal_node:
            #     return True                       # проверить, не является ли текущий узел целевым
            for child in node:  # все преемники текущего узла, ...
                if not visited[child]:  # ... которые ещё не были посещены ...
                    if self.check_attr(node.attrib):
                        child.attrib['parent_node']=node.attrib['name']
                    queue.append(child)  # ... добавить в конец очереди...
                    visited[child] = True  # ... и пометить как посещённые

    def create_item(self, node):
        if self.check_attr(node.attrib):
            Type = self.getType(node.attrib)
            item = Type(page=self, parent=self)
            item.setUpAttrib(node.attrib)
            self.items[item.name] = item
            if Type != GroupItem:
                self.addToGroup(item)

    def check_attr(self, attrib):
        name = attrib.get('name')
        return name is not None

    def getType(self, attrib):
        if attrib.get('type') is None:
            return self.ITEM_TYPES['other']
        else:
            return self.ITEM_TYPES[attrib['type']]

    def readXML(self, name):
        tree = self.gamePages.gameRoot.cfg.getXML_Page(name)
        self.xml_page:ET.Element = tree.getroot()

    def find_element(self, start_node, name = None, func = None):
        def plug(node):
            pass
        if func is None:
            func = plug
        visited = {}  # изначально список посещённых узлов пуст
        for node in start_node.iter():
            visited[node] = False
        queue = list()
        queue.append(start_node)  # начиная с узла-источника
        visited[start_node] = True
        while len(queue) != 0:  # пока очередь не пуста
            node = queue.pop()  # извлечь первый элемент в очереди
            func(node)
            if self.check_attr(node.attrib):
                if node.attrib['name'] == name:
                    return node
            for child in node:  # все преемники текущего узла, ...
                if not visited[child]:  # ... которые ещё не были посещены ...
                    queue.append(child)  # ... добавить в конец очереди...
                    visited[child] = True  # ... и пометить как посещённые

    def setDict(self, data):
        result = ''
        for k, v in data.items():
            result = result + k + ' : ' + v + '\n'
        return result
        
    @abstractmethod
    def setUp(self):
        """
        Устанавливаем настройки страницы
        """
        pass
    @abstractmethod
    def showPage(self):
        """
        Показать  страницу
        """
        pass
    @abstractmethod
    def updatePage(self):
        """
        Обновить страницу
        """
        pass

    @abstractmethod
    def addButton(self, arg):
        pass

    def checkFocus(self, pos):
        pass

    def resized(self):
        self.setPos(self.gamePages.gameRoot.view.mapToScene(0, 0))
        pass

    def release(self):
        pass

    def collisions(self, pos):
        pass

    def setUpGui(self):
        pass

    def destroy(self):
        pass

    # def mousePressEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent):
    #     super(AbstractPage, self).mousePressEvent(event)
    #     pass

    def mouseMoveEvent(self, e):
        pass

    def keyPressEvent(self, e):
        pass

    def resizeBackground(self, background):
        w_screen = self.gamePages.gameRoot.cfg.dev_size[0]
        w_pic = self.background.boundingRect().width()
        prec = 0
        if w_screen > w_pic:
            prec = w_pic / w_screen
        else:
            prec = w_screen /w_pic
        background.setScale(prec)
        x = (self.gamePages.gameRoot.cfg.dev_size[0] - self.background.boundingRect().width() * prec) / 2
        y = (self.gamePages.gameRoot.cfg.dev_size[1] - self.background.boundingRect().height() * prec) / 2
        background.setPos(x, y)

    def updatePos(self):
        """ update position for scale view"""
        self.setPos(self.gamePages.gameRoot.view.mapToScene(0, 0))



