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

from PySide2 import QtGui, QtCore, QtWidgets


class GamePages(object):
    """docstring for GamePages."""
    def __init__(self):
        super(GamePages, self).__init__()
        self.gameRoot = None
        # this is current page
        self.page = None
        self.focus = False
        self.pages = {}
        self.visiblePage = True



    def setGameRoot(self, gameRoot):
        self.gameRoot =  gameRoot
        self.gameRoot.gamePages = self

    def setUpPages(self):
        self.setUpCharecterPage()
        self.setUpGameMenu()

    def destroyPages(self):
        pages = list(self.pages.values())[:]
        keys = list(self.pages.keys())[:]
        i =0
        for page in pages:
            if keys[i] != 'startPage':
                page.destroy()
                print(keys[i], '-- destroy')
                if not page.scene() is None:
                    self.gameRoot.scene.removeItem(page)
                page = None
                del self.pages[keys[i]]
            i+=1
        self.pages = {}
        del self.gameMenu
        self.characterPage = None


    def setUpStartPage(self, ui):
        self.startPage = self.buildPage('startPage', StartPage)
        self.page = self.startPage
        # self.startPage.start.pressed.connect(ui.setDefaultGame)
        self.startPage.start.pressed.connect(ui.startGame)
        self.startPage.start.pressed.connect(self.startPage.startSlot)
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
        self.characterPage = self.buildPage('characterPage', CharacterPage)
        # self.gameRoot.controller.mousePress.connect(self.characterPage.mousePressEvent)
        # self.characterPage.pageUpdate()

    def buildPage(self, pageName, pageClass):
        page = pageClass(self)
        self.pages[pageName] = page
        self.gameRoot.controller.keyPress.connect(page.keyPressEvent)
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
            if not page is None:
                page.resized()

    def setCharacter(self, character):
        self.characterPage.character = character

