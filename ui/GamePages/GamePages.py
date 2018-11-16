"""
В это пакете находятся вызываемые страницы.
Страницы создаются один раз при загрузке игры.
Страницы обновляются по мере необходимости.
"""
from ui.GamePages.AbstractPage import AbstractPage
from ui.GamePages.StartPage import StartPage
from ui.GamePages.LevelSelect import LevelSelect
from ui.GamePages.GameMenuPage import GameMenuPage
from ui.GamePages.CharacterPage import CharacterPage
from ui.GamePages.PerksPage import PerksPage
from ui.GamePages.MasteriesPage import MasteriesPage

from PySide2 import QtGui, QtCore, QtWidgets


class GamePages(object):
    """docstring for GamePages."""
    def __init__(self):
        super(GamePages, self).__init__()
        self.gameRoot = None
        # this is current page
        self.focusState = False
        self.page = None
        self.focus = False
        self.pages = {}
        self.visiblePage = True



    def setGameRoot(self, gameRoot):
        self.gameRoot =  gameRoot
        self.gameRoot.gamePages = self

    def setUpPages(self):
        self.setUpCharecterPage()
        self.setUpPerksPage()
        self.setUpMasteriesPage()
        self.setUpGameMenu()

    def destroyPages(self):
        pages = list(self.pages.values())[:]
        keys = list(self.pages.keys())[:]
        i =0
        for page in pages:
            if not page.isService:
                page.destroy()
                print(keys[i], '-- destroy')
                if not page.scene() is None:
                    self.gameRoot.scene.removeItem(page)
                del self.pages[keys[i]]
            i += 1
        self.gameMenu = None


    def setUpStartPage(self, ui):
        self.startPage = self.buildPage('startPage', StartPage)
        self.page = self.startPage
        # self.startPage.newGame.pressed.connect(ui.setDefaultGame)
        self.startPage.stop.pressed.connect(ui.stopGame)

    def setUpLevelsPage(self):
        self.levelSelect = self.buildPage('levelSelect', LevelSelect)
        self.gameRoot.controller.mousePress.connect(self.levelSelect.mousePressEvent)

    def setUpGameMenu(self):
        gameMenu = self.buildPage('gameMenu', GameMenuPage)
        self.gameRoot.scene.addItem(gameMenu)
        gameMenu.setUpConsole()
        gameMenu.resized()
        self.gameMenu = gameMenu

    def setUpCharecterPage(self):
        characterPage = self.buildPage('characterPage', CharacterPage)
        self.gameRoot.controller.mousePress.connect(characterPage.mousePress)
        # self.characterPage.pageUpdate()

    def setUpPerksPage(self):
        perksPage = self.buildPage('perksPage', PerksPage)
        self.gameRoot.controller.mousePress.connect(perksPage .mousePress)

    def setUpMasteriesPage(self):
        masteriesPage = self.buildPage('masteriesPage', MasteriesPage)
        self.gameRoot.controller.mousePress.connect(masteriesPage .mousePress)


    def buildPage(self, pageName, pageClass):
        page = pageClass(self)
        self.pages[pageName] = page
        self.gameRoot.controller.keyPress.connect(page.keyPressEvent)
        page.focusable.connect(self.setFocus)
        page.setUpGui()
        return page



    def mouseMoveEvent(self, e):
        # self.checkFocus(e.pos())
        self.page.mouseMoveEvent(e)
        pass

    def mousePressEvent(self, e):
        # self.page.mousePressEvent(e)
        pass


    def resized(self):
        for page in self.pages.values():
            page.resized()

    def setCharacter(self, character):
        self.characterPage.character = character

    @property
    def isGamePage(self):
        if self.startPage.state:
            return True
        if self.levelSelect.state:
            return True

    def setFocus(self, isFocus):
        self.focusState = isFocus

    @property
    def isFocus(self):
        return self.focusState or self.gameMenu.isFocus()

