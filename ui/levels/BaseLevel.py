
class BaseLevel(object):
    def __init__(self):
        super(BaseLevel, self).__init__()
        self.gameRoot = None
        self.middleLayer = None
        self.world = None
        self.units = None

    def setGameRoot(self, gameRoot):
        self.gameRoot =  gameRoot
        self.gameRoot.level = self

    def setMiddleLayer(self, middleLayer):
        self.middleLayer = middleLayer
        self.middleLayer.level =  self

    def setGameWorld(self, world):
        self.world = world
        self.world.level = self

    def setUnits(self, units):
        self.units = units
        self.units.level = self
