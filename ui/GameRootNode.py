from LEngine import LEngine
from ui.gameconfig.GameConfiguration import GameConfiguration


class GameRootNode(object):
    """docstring for GameRootNode."""

    def __init__(self):
        super(GameRootNode, self).__init__()
        self.scene = None
        self.view = None
        self.cfg: GameConfiguration = None
        self.level = None
        self.loop = None
        self.levels = None
        self.gamePages = None
        self.game = None
        self.lengine: LEngine = None
        self.ui = None

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
        self.controller.setGameRoot(self)

    def setLevel(self, level):
        self.level = level
        self.level.setGameRoot(self)

    def setLevelFactory(self, factory):
        self.levelFactory = factory
        self.levelFactory.setGameRoot(self)

    def setGamePages(self, gamePages):
        self.gamePages = gamePages
        self.gamePages.gameRoot = self
