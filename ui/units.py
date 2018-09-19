from PySide2 import QtCore, QtWidgets

class GameObject(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, w = 1, h = 1):
        super(GameObject, self).__init__()
        self.worldPos = QtCore.QPoint()
        self.w = w
        self.h = h


    def setWorldX(self, x):
        self.worldPos.setX(x)
        self.setX(x * self.w)

    def setWorldY(self, y):
        self.worldPos.setY(y)
        self.setY(y * self.h)

    def setWorldPos(self, x, y):
        self.setWorldX(x)
        self.setWorldY(y)

    def getWorldPos(self):
        return self.worldPos.x(), self.worldPos.y(),

    def setDirection(self, x, y):
        pass



class GameToolTip(QtWidgets.QGraphicsRectItem):
    """docstring for GameToolTip."""
    def __init__(self, arg):
        super(GameToolTip, self).__init__()
        self.setRect(0, 0, 32, 32)


class BasicUnit(GameObject):
    """docstring for BasicUnit."""
    def __init__(self, *arg, gameconfig):
        super(BasicUnit, self).__init__(*arg)
        self.uid = 0
        self.gameconfig = gameconfig
        self.directionPix = self.gameconfig.getPicFile('DIRECTION POINTER.png')
        self.setUpDirections()
        self.activate = False
        self.hp = 100



    def setUpDirections(self):
        self.dirS = QtWidgets.QGraphicsPixmapItem(self)
        dirY = self.h - self.directionPix.height()
        dirX = (self.w / 2) - (self.directionPix.width() / 2)
        self.dirS.setPos(dirX, dirY)
        self.dirS.setPixmap(self.directionPix)
        self.dirS.setVisible(False)

        self.dirN = QtWidgets.QGraphicsPixmapItem(self)
        self.dirN.setPixmap(self.directionPix)
        dirY = self.directionPix.height()
        dirX = (self.w / 2) + (self.directionPix.width() / 2)
        self.dirN.setPos(dirX, dirY)
        self.dirN.setRotation(180.0)
        self.dirN.setVisible(False)

        self.dirW = QtWidgets.QGraphicsPixmapItem(self)
        self.dirW.setPixmap(self.directionPix)
        dirY = (self.h / 2) - (self.directionPix.height() / 2)
        dirX = self.directionPix.width()
        self.dirW.setPos(dirX, dirY)
        self.dirW.setRotation(90.0)
        self.dirW.setVisible(False)


        self.dirO = QtWidgets.QGraphicsPixmapItem(self)
        self.dirO.setPixmap(self.directionPix)
        dirY = (self.h / 2) + (self.directionPix.height() / 2)
        dirX = self.w - self.directionPix.width()
        self.dirO.setPos(dirX, dirY)
        self.dirO.setRotation(-90.0)
        self.dirO.setVisible(False)


    def setDirection(self, x, y):
        if y >= 1 and x == 0:
            self.dirS.setVisible(True)
            self.dirN.setVisible(False)
            self.dirW.setVisible(False)
            self.dirO.setVisible(False)
        elif y <= -1 and x == 0:
            self.dirS.setVisible(False)
            self.dirN.setVisible(True)
            self.dirW.setVisible(False)
            self.dirO.setVisible(False)
        if x >= 1 and y == 0:
            self.dirS.setVisible(False)
            self.dirN.setVisible(False)
            self.dirW.setVisible(False)
            self.dirO.setVisible(True)
        elif x <= -1 and y == 0:
            self.dirS.setVisible(False)
            self.dirN.setVisible(False)
            self.dirW.setVisible(True)
            self.dirO.setVisible(False)

    def __eq__(self, other):
        return self.worldPos.x == other.worldPos.x and self.y == other.worldPos.y

    def __hash__(self):
        return hash(self.worldPos.x*10000 + self.worldPos.y)



class SelectItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *arg):
        super(SelectItem, self).__init__(*arg)
        self.setBrush(QtCore.Qt.cyan)
        self.setOpacity(0.3)

class Units(QtWidgets.QGraphicsItemGroup):
    """docstring for Units."""
    def __init__(self, *arg):
        super(Units, self).__init__(*arg)
        self.active_unit = None
        self.units_location = {}
        self.units_at = {}
        self.units_bf = {}
        self.units_stack = None

    def getUitsLocations(self):
        for uid, unit in self.units_at.items():
            if uid != self.active_unit.uid:
                yield unit.getWorldPos()

    def getUnit(self, x, y):
        """ get unit from point x, y """
        return self.units_location.setdefault((x, y), None)

    # def updateLocationsDungeon(self, unit, pos)

    def updateLocations(self, unit, pos):
        del self.units_location[pos]
        self.units_location[(unit.worldPos.x(), unit.worldPos.y())] = unit

    def collisionHeorOfUnits(self, x = None, y = None):
        pos = None
        if x is None:
            if not (self.active_unit.worldPos.x(), y) in self.getUitsLocations():
                pos = (self.active_unit.worldPos.x(), self.active_unit.worldPos.y())
                self.active_unit.setWorldY(y)
                self.updateLocations(self.active_unit, pos)
        elif y is None:
            if not (x, self.active_unit.worldPos.y()) in self.getUitsLocations():
                pos = (self.active_unit.worldPos.x(), self.active_unit.worldPos.y())
                self.active_unit.setWorldX(x)
                self.updateLocations(self.active_unit, pos)

    def removeUnit(self, uid):
        unit = self.units_at[uid]
        self.removeFromGroup(unit)
        del self.units_location[(unit.worldPos.x(), unit.worldPos.y())]
        self.locations.remove(unit.worldPos)
        del self.units_bf[uid]
        del self.units_at[uid]

    def setActiveUnit(self, unit):
        self.active_unit = self.units_at[unit.uid]

    def setUnitStack(self, units):
        self.units_stack = units
