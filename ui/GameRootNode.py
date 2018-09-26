
class GameRootNode(object):
    """docstring for GameRootNode."""
    def __init__(self):
        super(GameRootNode, self).__init__()
        self.currentLevel = None
        self.levels = None
        self.gamePages = None

    def setCurrentLevel(self, level):
        self.currentLevel = level
        self.currentLevel.setGameRoot(self)

    def setGamePages(self, gamePages):
        self.gamePages = gamePages
        self.gamePages.setGameRoot(self)
