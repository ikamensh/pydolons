from PySide2 import QtCore
from .characterpage import CharacterPage, CharacterModel

class PageManager(object):
    """docstring for PageManager."""
    def __init__(self, gameconfig):
        super(PageManager, self).__init__()
        self.gameconfig = gameconfig
        self.pages = {}
        self.active_pages = {}
        self.character_model = CharacterModel()
        self.character_page = CharacterPage(gameconfig)
        self.character_page.model = self.character_model

    def setHero(self, hero):
        self.character_model.setHero(hero)
        self.character_page.pageUpdate()
        # self.character_page.update()

    def setScene(self, scene):
        self.scene = scene

    def update(self):
        self.character_model.update()
        self.character_page.pageUpdate()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_M:
            # self.character_page.setVisible(True)
            self.update()
            self.scene.addItem(self.character_page)
            return True
        if e.key() == QtCore.Qt.Key_Escape:
            # self.character_page.setVisible(False)
            self.scene.removeItem(self.character_page)
            return False

    def mousePressEvent(self, e, pos):
        self.character_page.widgetFactory.collisions(pos)
        self.character_page.pageUpdate()

    def mouseReleaseEvent(self, e, pos):
        self.character_page.widgetFactory.release()
        self.character_page.pageUpdate()
