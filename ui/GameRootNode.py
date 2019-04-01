from __future__ import annotations

from LEngine import LEngine
from ui.gameconfig.GameConfiguration import GameConfiguration


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from DreamGame import DreamGame
    from ui.GamePages import GamePages
    from ui.levels.BaseLevel import BaseLevel
    from ui.levels.LevelFactory import LevelFactory
    from ui.GameController import GameController
    from ui.TheUI import TheUI
    from PySide2.QtWidgets import QGraphicsScene
    from PySide2.QtWidgets import QGraphicsView


class GameRootNode(object):
    """docstring for GameRootNode."""
    def __init__(self):
        super(GameRootNode, self).__init__()
        self.scene:QGraphicsScene = None
        self.view:QGraphicsView = None
        self.controller:GameController = None
        self.cfg:GameConfiguration = None
        self.level:BaseLevel = None
        self.levelFactory:LevelFactory = None
        self.gamePages:GamePages = None
        self.game:DreamGame = None
        self.lengine:LEngine = None
        self.loop = None
        self.ui:TheUI = None

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
