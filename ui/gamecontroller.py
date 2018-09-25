from PySide2 import QtCore, QtGui, QtWidgets


class GameController:
    def __init__(self, gameconfig, game, view, scene, menu):

        self.gameconfig = gameconfig
        self.the_game = game
        self.view = view
        self.scene = scene
        self.screenMenu = menu

        self.tr = QtGui.QTransform()

        self.cursor = QtWidgets.QGraphicsEllipseItem(-10, -10, 20, 20)

        self.last_point = (0, 0)
        self.selected_point = None


    def setUp(self, world, units, middleLayer):
        self.world = world
        self.units = units
        self.middleLayer = middleLayer

    def moveCursor(self, newPos):
        self.cursor.setX(newPos.x())
        self.cursor.setY(newPos.y())

    def mouseMoveEvent(self, e):
        """ Метод перехватывает событие движение мыши
        """
        newPos = self.view.mapToScene(e.x(), e.y())
        self.moveCursor(newPos)
        self.itemSelect(newPos)

    def mousePressEvent(self, e):
        self.the_game.ui_order( (self.last_point[0], self.last_point[1]) )
        self.updateWorld()
        self.selected_point = self.last_point
        self.middleLayer.showSelectedItem(self.selected_point)

    def keyPressEvent(self, e):
        pass
        # self.attackUnit(e)
        # self.setFacingHero(e)
        # self.moveUnit(e)
        # self.tabUnit(e)

    def wheelEvent(self, e):
        """ Метод перехватывает событие мышки скролл, скролл больше 0 зумм +,
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
                self.middleLayer.removeUnitLayer(uid)
                self.screenMenu.updateUnitStack(uid)
            else:
                cell = self.the_game.battlefield.unit_locations.setdefault(unit, None)
                if not cell is None:
                    pos = (self.units.units_at[uid].worldPos.x, self.units.units_at[uid].worldPos.y)
                    self.units.units_at[uid].setWorldPos(cell.x , cell.y )
                    self.units.updateLocations(self.units.units_at[uid], pos)
        self.middleLayer.updateSupport()


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
        self.middleLayer.updateSupport()

    def zoomIn(self):
        self.tr.scale(1.05, 1.05)
        self.world.setTransform(self.tr)
        self.middleLayer.setTransform(self.tr)
        self.units.setTransform(self.tr)

    def zoomOut(self):
        self.tr.scale(1/1.05, 1/1.05)
        self.world.setTransform(self.tr)
        self.middleLayer.setTransform(self.tr)
        self.units.setTransform(self.tr)

    def moveScene(self, rect, x, y):
        rect.translate(x, y)
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

        if e.x() + 5.0 > self.view.viewport().width() - 5.0:
            rect.translate(10, 0)
            self.scene.setSceneRect(rect)
            self.screenMenu.setDefaultPos()

        if e.y() - 5.0 < 5.0:
            rect.translate(0, -10)
            self.scene.setSceneRect(rect)
            self.screenMenu.setDefaultPos()

        if e.y() + 5.0 > self.view.viewport().height() - 5.0:
            rect.translate(0, 10)
            self.scene.setSceneRect(rect)
            self.screenMenu.setDefaultPos()




    def itemSelect(self, newPos):

        x = int((newPos.x() / self.tr.m11()) / self.gameconfig.unit_size[0])
        if newPos.x() < 0:
            x -= 1

        y = int((newPos.y() / self.tr.m11()) / self.gameconfig.unit_size[1])
        if newPos.y() < 0:
             y -= 1

        world_x, world_y = self.gameconfig.world_size
        if 0 <= x < world_x and  0 <= y < world_y:
            self.last_point = x, y

        self.middleLayer.showToolTip(self.last_point)
        self.middleLayer.showSelectItem(self.last_point)
