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
        self.characterPage.setPos(280, 65)
        self.characterPage.gamePages = self
        self.characterPage.setUpGui()
        self.characterPage.pageUpdate()

    def showPage(self, pageName):
        assert(pageName, str)
        if pageName == 'CharacterPage' and not self.characterPage.state:
            x, y = 0, 0
            self.gameRoot.scene.addItem(self.characterPage)
            if self.gameRoot.cfg.dev_size[0] > 800:
                x = (self.gameRoot.cfg.dev_size[0] - self.characterPage.w)/2
                y = (self.gameRoot.cfg.dev_size[1] - self.characterPage.h)/2
            print(x, y)
            # self.characterPage.setPos(int(x), int(y))
            self.characterPage.pageUpdate()
            self.characterPage.state = True
    def close(self):
        if self.characterPage.state:
            self.gameRoot.scene.removeItem(self.characterPage)
            self.characterPage.state = False


    def updateGui(self):
        self.gameMenu.updateGui()
