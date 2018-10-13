
class GameRootNode(object):
    """docstring for GameRootNode."""
    def __init__(self):
        super(GameRootNode, self).__init__()
        self.scene = None
        self.view = None
        self.cfg = None
        self.level = None
        self.levels = None
        self.gamePages = None
        self.game = None


    def setView(self, view):
        self.view = view
        self.view.gameRoot = self

    def setScene(self, scene):
        self.scene = scene
        self.scene.gameRoot = self

    def setGameConfig(self, gameConfig):
        self.cfg = gameConfig
        self.cfg.gameRoot = self

    def setGameController(self, controller):
        self.controller = controller
        self.controller.gameRoot = self



    def setLevel(self, level):
        self.level = level
        self.level.setGameRoot(self)

    def setGamePages(self, gamePages):
        self.gamePages = gamePages
        self.gamePages.gameRoot = self
