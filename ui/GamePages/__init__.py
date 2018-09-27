"""
В это пакете находятся вызываемые страницы.
Страницы создаются один раз при загрузке игры.
Страницы обновляются по мере необходимости.
"""

from ui.GamePages.GameMenuPage import ScreenMenu

class GamePages(object):
    """docstring for GamePages."""
    def __init__(self):
        super(GamePages, self).__init__()
        self.gameRoot = None

    def setGameRoot(self, gameRoot):
        self.gameRoot =  gameRoot

    def setUpGameMenu(self):
        self.gameMenu = ScreenMenu()
        self.scene.addItem(self.gameMenu)
        self.gameMenu.setUpGui()
        self.gameMenu.setUpConsole()


    def updateGui(self):
        self.gameMenu.updateGui()
