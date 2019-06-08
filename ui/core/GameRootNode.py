from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.core.gameconfig.GameConfiguration import GameConfiguration
    from ui.core.LEngine import LEngine
    from DreamGame import DreamGame
    from ui.pages import GamePages
    from ui.pages import WidgetFactory
    from ui.core.levels.BaseLevel import BaseLevel
    from ui.core.levels.LevelFactory import LevelFactory
    from ui.core.GameController import GameController
    from ui.core.TransformSupport import TransformSupport
    from ui.TheUI import TheUI
    from PySide2.QtWidgets import QGraphicsScene
    from ui.core.GameView import GameView
    from ui.core.GameLoopThread import GameLoopThread


class GameRootNode(object):
    """docstring for GameRootNode."""
    def __init__(self):
        super(GameRootNode, self).__init__()
        self.scene: QGraphicsScene = None
        self.view: GameView = None
        self.controller: GameController = None
        self.cfg: GameConfiguration = None
        self.level: BaseLevel = None
        self.levelFactory: LevelFactory = None
        self.gamePages: GamePages = None
        self.game: DreamGame = None
        self.lengine: LEngine = None
        self.loop: GameLoopThread = None
        self.ui: TheUI = None
        self.widgetFactory: WidgetFactory =None
        self.tr_support: TransformSupport = None

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
