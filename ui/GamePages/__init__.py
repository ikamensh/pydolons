"""
В это пакете находятся вызываемые страницы.
Страницы создаются один раз при загрузке игры.
Страницы обновляются по мере необходимости.
"""

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
        self.setUpCharecterPage()
        self.setUpGameMenu()

    def setUpGameMenu(self):
        self.gameMenu = ScreenMenu()
        self.gameRoot.scene.addItem(self.gameMenu)
        self.gameMenu.setGameRoot(self.gameRoot)
        self.gameMenu.setUpGui()
        self.gameMenu.setUpConsole()

    def setUpCharecterPage(self):
        self.characterPage = CharacterPage()
        self.characterPage.gamePages = self
        self.characterPage.setUpGui()

    def updateGui(self):
        self.gameMenu.updateGui()
