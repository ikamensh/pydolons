"""
В это пакете находятся вызываемые страницы.
Страницы создаются один раз при загрузке игры.
Страницы обновляются по мере необходимости.
"""
from ui.GamePages.AbstractPage import AbstractPage
from ui.GamePages.StartPage import StartPage
from ui.GamePages.GameMenuPage import ScreenMenu
from ui.GamePages.CharacterPage import CharacterPage

class GamePages(object):
    """docstring for GamePages."""
    def __init__(self):
        super(GamePages, self).__init__()
        self.gameRoot = None
        # this is current page
        self.page = None
        self.unit = None
        self.focus = False


    def setGameRoot(self, gameRoot):
        self.gameRoot =  gameRoot
        self.gameRoot.gamePages = self

    def setUpPages(self):
        self.setUpStartPage()
        self.setUpCharecterPage()
        self.setUpGameMenu()

    def setUpStartPage(self):
        self.startPage = StartPage()
        self.startPage.arg = 213

    def setUpGameMenu(self):
        self.gameMenu = ScreenMenu()
        self.gameRoot.scene.addItem(self.gameMenu)
        self.gameMenu.setGameRoot(self.gameRoot)
        self.gameMenu.setUpGui()
        self.gameMenu.setUpConsole()

    def setUpCharecterPage(self):
        self.characterPage = CharacterPage()
        self.characterPage.setPos(0, 0)
        self.characterPage.gamePages = self
        self.characterPage.setUpGui()
        self.characterPage.pageUpdate()

    def showPage(self, pageName):
        """
        This is bug transformation item to scene

        How to get x, y for item in scene ?

        if screen size = 420, 340
        page size = 100, 50
        correct x, y = ((420 - 100) / 2) /2, ((320 - 50) / 2) /2
        x, y = (420 - 50) / 4, (320 - 50) / 4
        """
        assert isinstance(pageName, str)
        if pageName == 'CharacterPage' and not self.characterPage.state:
            x, y = 0, 0
            self.gameRoot.scene.addItem(self.characterPage)
            self.page = self.characterPage
            if self.gameRoot.cfg.dev_size[0] > 800:
                x = (self.gameRoot.cfg.dev_size[0] - self.characterPage.w) / 4
                y = (self.gameRoot.cfg.dev_size[1] - self.characterPage.h) / 4
            self.characterPage.setPos(int(x), int(y))
            self.characterPage.pageUpdate()
            self.characterPage.state = True

    def close(self):
        if self.characterPage.state:
            self.gameRoot.scene.removeItem(self.characterPage)
            self.page = None
            self.characterPage.state = False

    def collision(self, pos):
        self.gameMenu.collision(pos)
        if not self.page is None:
            self.page.widgetFactory.collisions(pos)

    def mousePressEvent(self, pos):
        if not self.page is None:
            self.page.collisions(pos)

    def mouseReleaseEvent(self):
        if not self.page is None:
            self.page.release()

    def updateGui(self):
        self.gameMenu.updateGui()

    def setHeroUnit(self, unit):
        self.unit = unit
        self.characterPage.unit = unit

    def setCharacter(self, character):
        self.characterPage.character = character

    def checkFocus(self, pos):
        self.focus = self.gameMenu.checkFocus(pos)

    # @property
    # def focus(self):
    #     return self.gameMenu.focus
