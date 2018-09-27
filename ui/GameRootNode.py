
class GameRootNode(object):
    """docstring for GameRootNode."""
    def __init__(self):
        super(GameRootNode, self).__init__()
        self.level = None
        self.levels = None
        self.gamePages = None

    def setLevel(self, level):
        self.level = level
        self.level.setGameRoot(self)

    def setGamePages(self, gamePages):
        self.gamePages = gamePages
        self.gamePages.setGameRoot(self)
