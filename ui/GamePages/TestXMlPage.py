from ui.GamePages.AbstractPage import AbstractPage
from ui.GamePages.suwidgets.TestItem import TestItem
from ui.GamePages.suwidgets.TextItem import TextItem
from ui.GamePages.suwidgets.GroupItem import GroupItem
from ui.GamePages.suwidgets.perk_tree.GamePerkTree import GamePerkTree
from xml.etree import ElementTree as ET
from PySide2.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent
from PySide2 import QtCore

"""
str.png
agi.png
end.png
prc.png
int.png
cha.png
strange_perk.png
strange_perk.png
strange_perk.png
strange_perk.png


{1: 'Gifted: streingth I', 2: 'Gifted: streingth II', 3: 'Gifted: streingth III'}
{1: 'Gifted: agility I', 2: 'Gifted: agility II', 3: 'Gifted: agility III'}
{1: 'Gifted: endurance I', 2: 'Gifted: endurance II', 3: 'Gifted: endurance III'}
{1: 'Gifted: perception I', 2: 'Gifted: perception II', 3: 'Gifted: perception III'}
{1: 'Gifted: intelligence I', 2: 'Gifted: intelligence II', 3: 'Gifted: intelligence III'}
{1: 'Gifted: charisma I', 2: 'Gifted: charisma II', 3: 'Gifted: charisma III'}
{1: 'Unusual health I', 2: 'Superior health II', 3: 'Incredible health III'}
{1: 'Unusual mana I', 2: 'Superior mana II', 3: 'Incredible mana III'}
{1: 'Unusual stamina I', 2: 'Superior stamina II', 3: 'Incredible stamina III'}
{1: 'Unusual initiative I', 2: 'Superior initiative II', 3: 'Incredible initiative III'}


CLUB club.png
SWORD sword.png
AXE axe.png
DAGGER dagger.png
SPEAR spear.png
UNARMED unarmed.png
BOW bow.png
HAMMER hammer.png
SHOOT shoot.png

FROST frost.png
FIRE fire.png
LIGHT light.png

LIGHTNING lightning.png
EARTH earth.png
ACID acid.png

SONIC sonic.png
ASTRAL astral.png
MIND mind.png

HOLY holy.png
DARK dark.png
NATURE nature.png

        <item name="mastery_block_total_xp"
                          position="inherit"
                          left = '10'
                          top = '32'
                          width="404"
                          height="10"
                          text="Total xp: 0"
                          color="#FFFFFF"
                          font_size="20"
                          type="text">
                    </item>

STREINGTH streingth.png
ENDURANCE endurance.png
AGILITY agility.png
PERCEPTION perception.png
INITIATIVE initiative.png
CHARISMA charisma.png
"""


class XMLPage(AbstractPage):
    ITEM_TYPES = {'other':TestItem, 'text':TextItem, 'group':GroupItem}
    def __init__(self, gamePages):
        super(XMLPage, self).__init__(gamePages)
        self.xml_page = None
        self.items = {}
        self.elements = {}
        self.readXML()
        self.gamePages.gameRoot.view.wheel_change.connect(self.updatePos)
        self.name = 'XMLPage'
        # self.perk_tree(self.gamePages.gameRoot)
        pass

    def perk_tree(self, root):
        cha = root.lengine.character
        self.gpt = GamePerkTree(root.cfg, cha.perk_trees[0], cha)
        print(list(self.gpt.get_perks()))

    def keyPressEvent(self, e):
        pass

    def setUpGui(self):
        self.read_tree(self.xml_page)

    def readXML(self):
        xml_path = '/home/reef/PycharmProjects/pydolons/resources/pages/test_page.xml'
        tree = ET.parse(xml_path)
        self.xml_page:ET.Element = tree.getroot()

    def read_tree(self, start_node):
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

    def sceneEvent(self, event:QtCore.QEvent):
        if event.type() is QtCore.QEvent.GraphicsSceneMousePress:
            self.pressItem(self.scene().itemAt(event.scenePos(), self.scene().views()[0].transform()))
            return True
        elif event.type() is QtCore.QEvent.GraphicsSceneMouseRelease:
            self.releaseItem(self.scene().itemAt(event.scenePos(), self.scene().views()[0].transform()))
            return True
        elif isinstance(event, QGraphicsSceneHoverEvent):
            self.hoverItem(self.scene().itemAt(event.scenePos(), self.scene().views()[0].transform()))
            return True
        else:
            print(event)
            return super(XMLPage, self).sceneEvent(event)

    def pressItem(self, item):
        if item is not None:
            print(item.name, 'press')

    def releaseItem(self, item):
        if item is not None:
            print(item.name, 'release')
            if item.input == 'button':
                if item.name[0:4] == 'perk':
                    self.perk_up(item.name[5:-3])

    def hoverItem(self, item):
        if item is not None:
            print(item.name, 'hover')


    # def sceneEventFilter(self, watched:QGraphicsItem, event:QtCore.QEvent):
    #     return True
    #
    # def mouseReleaseEvent(self, event:QGraphicsSceneMouseEvent):
    #     # print(event)
    #     super(XMLPage, self).mouseReleaseEvent(event)
    #     pass
    #
    # def mousePressEvent(self, event:QGraphicsSceneMouseEvent):
    #     # print(event)
    #     super(XMLPage, self).mousePressEvent(event)
    #     pass
    #
    # def mouseMoveEvent(self, event:QGraphicsSceneMouseEvent):
    #     # print(event)
    #     super(XMLPage, self).mouseMoveEvent(event)
    #     pass


