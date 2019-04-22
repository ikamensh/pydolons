"""
В это пакете находятся вызываемые страницы.
Страницы создаются один раз при загрузке игры.
Страницы обновляются по мере необходимости.
"""
from __future__ import annotations


from ui.pages.StartPage import StartPage
from ui.pages.LevelSelect import LevelSelect
from ui.pages.GameMenuPage import GameMenuPage
from ui.pages.character_page.CharacterPage import CharacterPage
from ui.pages.inventory_page.InventoryPage import InventoryPage
from ui.pages.BackGorundPage import BackGorundPage
from ui.pages.ReadmePage import ReadmePage
from ui.pages.SettingsPage import SettingsPage
from ui.pages.WidgetFactory import WidgetFactory

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.core.GameRootNode import GameRootNode
    from ui.pages import AbstractPage


class GamePages(object):
    """docstring for pages."""
    def __init__(self):
        super(GamePages, self).__init__()
        self.gameRoot:GameRootNode = None
        # this is current page
        self.focusState = False
        self.focus = False
        # init pages
        self.pages = {}
        self.page: AbstractPage = None
        self.gameMenu: GameMenuPage = None
        self.background: BackGorundPage = None
        self.startPage: StartPage = None
        self.levelSelect: LevelSelect = None
        self.readme: ReadmePage = None
        self.characterPage: CharacterPage = None
        self.settigsPage: SettingsPage = None
        self.visiblePage = True

    def setGameRoot(self, gameRoot):
        self.gameRoot = gameRoot
        self.gameRoot.gamePages = self

    def setUpPages(self):
        self.setUpBackgrounPage()
        self.setUpGameMenu()
        self.gameRoot.scene.addItem(self.toolTip)
        self.gameRoot.scene.addItem(self.notify)
        self.setUpInventoryPage()
        self.gameRoot.scene.removeItem(self.startPage)
        self.gameRoot.scene.addItem(self.startPage)
        self.gameRoot.scene.removeItem(self.startPage.mainWidget)
        self.gameRoot.scene.addItem(self.startPage.mainWidget)

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
        self.gameRoot.scene.removeItem(self.toolTip)
        self.gameRoot.scene.removeItem(self.notify)

    def setUpBackgrounPage(self):
        self.background = self.buildPage('background', BackGorundPage)
        self.gameRoot.scene.addItem(self.background)

    def setUpStartPage(self, ui):
        self.startPage = self.buildPage('startPage', StartPage)
        self.page = self.startPage
        self.toolTip = WidgetFactory.getToolTip(self.gameRoot, w = 128, h = 0, opacity=1.)
        self.toolTip.gameRoot = self.gameRoot
        self.gameRoot.view.wheel_change.connect(self.toolTip.wheel_change)
        self.notify = WidgetFactory.getNotifyText(self.gameRoot)

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
        self.gameRoot.scene.addItem(characterPage)
        characterPage.showPage()

    def setUpInventoryPage(self):
        inventoryPage = self.buildPage('inventoryPage', InventoryPage)
        self.gameRoot.scene.addItem(inventoryPage)
        inventoryPage.hidePage()
        # self.gameRoot.controller.mouseMove.connect(inventoryPage.mouseMoveEvent)

    def setUpReadmePage(self):
        self.readme = self.buildPage('readmePage', ReadmePage)

    def setUpSettingsPage(self):
        self.settigsPage = self.buildPage('settigsPage', SettingsPage)

    def buildPage(self, pageName, pageClass):
        print('Init page:', pageName)
        page = pageClass(self)
        self.pages[pageName] = page
        self.gameRoot.view.keyPress.connect(page.keyPressEvent)
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
        if self.settigsPage.state:
            return True
        if not self.pages.get('chaPage') is None:
            if self.pages.get('chaPage').state:
                return True
        if not self.pages.get('gameMenu') is None:
            if self.pages.get('gameMenu').isFocus():
                return True

    def setFocus(self, isFocus):
        self.focusState = isFocus

    @property
    def isFocus(self):
        return self.focusState or self.gameMenu.isFocus()


