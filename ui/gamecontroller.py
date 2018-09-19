from PySide2 import QtCore, QtGui, QtWidgets


class GameController:
    """docstring for GameController."""
    def __init__(self, gameconfig, game):
        self.gameconfig = gameconfig
        self.the_game = game
        self.view = None
        self.tr = QtGui.QTransform()

        self.cursor = QtWidgets.QGraphicsEllipseItem(-10, -10, 20, 20)

        self.last_point = (0, 0)
        self.selected_point = None


    def setScreenMenu(self, menu):
        self.screenMenu = menu

    def setView(self, view):
        self.view = view

    def setUp(self, world, units, midleLayer):
        self.world = world
        self.units = units
        self.midleLayer = midleLayer

    def moveCursor(self, newPos):
        self.cursor.setX(newPos.x())
        self.cursor.setY(newPos.y())

    def mouseMoveEvent(self, e):
        """ Метод перехватывает событие движение мыши
        """
        newPos = self.view.mapToScene(e.x(), e.y())
        self.moveCursor(newPos)
        self.translateScene(e)
        self.itemSelect(newPos)

    def mousePressEvent(self, e):
        self.the_game.ui_order( (self.last_point[0] +4, self.last_point[1] +4) )
        self.updateWorld()
        self.selected_point = self.last_point
        self.midleLayer.showSelectedItem(self.selected_point)

    def resizeEvent(self, e):
        self.screenMenu.resize(self.view)

    def keyPressEvent(self, e):
        self.attackUnit(e)
        self.setFacingHero(e)
        # self.moveUnit(e)
        self.tabUnit(e)

    def wheelEvent(self, e):
        """ Метод перехватывает собитие мышки скролл, скролл больше 0 зумм +,
        скролл меньше нуля зумм -
        """
        if e.delta() > 0.0:
            self.zoomIn()
        elif e.delta() < 0.0:
            self.zoomOut()

    def updateWorld(self):
        for uid, unit in list(self.units.units_bf.items()):
            if not unit.alive:
                print('not live:', unit)
                self.units.removeUnit(uid)
                self.midleLayer.removeUnitLayer(uid)
                self.screenMenu.updateUnitStack(uid)
            else:
                cell = self.the_game.battlefield.unit_locations.setdefault(unit, None)
                if not cell is None:
                    pos = (self.units.units_at[uid].worldPos.x(), self.units.units_at[uid].worldPos.y())
                    self.units.units_at[uid].setWorldPos(cell.x - 4, cell.y - 4)
                    self.units.updateLocations(self.units.units_at[uid], pos)
        self.midleLayer.updateSupport()

    def attackUnit(self, e):
        if e.key() == QtCore.Qt.Key_E:
            if self.units.units_location.get(self.last_point):
                self.manager.attackHero(self.last_point)
                self.updateWorld()
            else:
                self.screenMenu.showNotify('Empty')


    def moveUnit(self, e):
        """ Управление двжением героя
        """
        if e.key() == QtCore.Qt.Key_W:
            print('up')
        if e.key() == QtCore.Qt.Key_S:
            print('down')
        if e.key() == QtCore.Qt.Key_A:
            print('left')
        if e.key() == QtCore.Qt.Key_D:
            print('right')
        self.midleLayer.updateSupport()

    def zoomIn(self):
        # self.view.scale(1.1, 1.1)
        # print(self.view.transform())
        self.tr.scale(1.1, 1.1)
        # print(self.tr)
        self.world.setTransform(self.tr)
        self.midleLayer.setTransform(self.tr)
        self.units.setTransform(self.tr)

    def zoomOut(self):
        # self.view.scale(1/1.1, 1/1.1)
        # print(self.view.transform())
        self.tr.scale(1/1.1, 1/1.1)
        self.world.setTransform(self.tr)
        self.midleLayer.setTransform(self.tr)
        self.units.setTransform(self.tr)

    def moveScene(self, rect, x, y):
        rect.translate(-10, 0)
        self.scene.setSceneRect(rect)
        self.screenMenu.setDefaultPos()

    def translateScene(self, e):
        """Данный метод обеспечивает перемещение сцены внутри представления
         метод проверяет приблизился ли курсор к краю представления
        """

        rect = self.scene.sceneRect()
        if e.x() - 5.0 < 5.0:
            rect.translate(-10, 0)
            self.scene.setSceneRect(rect)
            self.screenMenu.setDefaultPos()
            #
            # self.screenMenu.setX(self.screenMenu.x() - 10)
        if e.x() + 5.0 > self.view.viewport().width() - 5.0:
            rect.translate(10, 0)
            self.scene.setSceneRect(rect)
            self.screenMenu.setDefaultPos()
            #
            # self.screenMenu.setX(self.screenMenu.x() + 10)
        if e.y() - 5.0 < 5.0:
            rect.translate(0, -10)
            self.scene.setSceneRect(rect)
            self.screenMenu.setDefaultPos()
            #
            # self.screenMenu.setY(self.screenMenu.y() - 10)
        if e.y() + 5.0 > self.view.viewport().height() - 5.0:
            rect.translate(0, 10)
            self.scene.setSceneRect(rect)
            self.screenMenu.setDefaultPos()
            #
            # self.screenMenu.setY(self.screenMenu.y() + 10)




    def itemSelect(self, newPos):
        # last_point = 0, 0
        if newPos.x() < 0:
            x = int((newPos.x() / self.tr.m11()) / self.gameconfig.unit_size[0]) - 1
        else:
            x = int((newPos.x() / self.tr.m11()) / self.gameconfig.unit_size[0])

        if newPos.y() < 0:
            y = int((newPos.y() / self.tr.m11()) / self.gameconfig.unit_size[1]) - 1
        else:
            y = int((newPos.y() / self.tr.m11()) / self.gameconfig.unit_size[1])

        if x < self.gameconfig.world_a_size[0] and x >= -self.gameconfig.world_a_size[0] and y < self.gameconfig.world_a_size[1] and y >= -self.gameconfig.world_a_size[1]:
            self.last_point = x, y

        self.midleLayer.showToolTip(self.last_point)
        self.midleLayer.showSelectItem(self.last_point)

