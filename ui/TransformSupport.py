from battlefield import Cell
from PySide2 import QtCore, QtGui, QtWidgets
from math import fabs


class TransformSupport:

    def __init__(self, gameRoot):
        # super(World, self).__init__()
        self.gameRoot = gameRoot
        self.gameRoot.tr_support = self
        self.cfg = gameRoot.cfg
        self.level = None
        # Transform for ground
        self.tr = QtGui.QTransform()
        # Transform from ground
        self.tr_from_map = QtGui.QTransform()
        # Upate transform for new dev_size
        self.updadte_tr()
        self.scr_w = self.cfg.dev_size[0]
        self.scr_h = self.cfg.dev_size[1]

        self.frame_rect = QtCore.QRectF(0, 0, 1, 1)
        self.floor_rect = QtCore.QRect(0, 0, 1, 1)
        self.moveTimer = QtCore.QTimer()
        # Offset for map
        self.off = 32
        self.l_mouse = False
        self.isMovable = False

    def setItemPos(self, item, x, y):
        # item.setPos(x - (item.rect().x() + self.tr.m31()),
        #             y - (item.rect().y() + self.tr.m32()))
        item.setPos(x - (item.boundingRect().x() + self.tr.m31()),
                    y - (item.boundingRect().y() + self.tr.m32()))

    def getItemCoords(self, item):
        # return item.rect().x() + self.tr.m31() + item.pos().x(),\
        #        item.rect().y() + self.tr.m32() + item.pos().y(), \
        #        item.rect().x() + self.tr.m31() + item.pos().x() + item.rect().width(),\
        #        item.rect().y() + self.tr.m32() + item.pos().y() + item.rect().height()
        return item.boundingRect().x() + self.tr.m31() + item.pos().x(),\
            item.boundingRect().y() + self.tr.m32() + item.pos().y(), \
            item.boundingRect().x() + self.tr.m31() + item.pos().x() + item.boundingRect().width(),\
            item.boundingRect().y() + self.tr.m32() + item.pos().y() + item.boundingRect().height()

    def updadte_tr(self):
        """Update transform for new dev_size
        """
        self.tr.translate(-self.tr.m31(), -self.tr.m32())
        self.tr.translate(self.cfg.dev_size[0] / 2, self.cfg.dev_size[1] / 2)

    def initLevel(self, level):
        self.level = level
        self.tr.translate(-self.tr.m31(), -self.tr.m32())
        self.tr.translate(self.cfg.dev_size[0] / 2, self.cfg.dev_size[1] / 2)
        self.tr.translate(-level.world.floor.rect().width() /
                          2, -level.world.floor.rect().height() / 2)
        level.world.setTransform(self.tr)
        self.floor_rect.setRect(level.world.pos().x() + self.tr.m31(),
                                level.world.pos().y() + self.tr.m32(),
                                level.world.floor.rect().width() - 2,
                                level.world.floor.rect().height() - 2)
        level.units.setTransform(self.tr)
        level.gameVision.setTransform(self.tr)
        level.middleLayer.setTransform(self.tr)
        self.update_frame_rect()

    def setMovableMaps(self):
        if self.isMovable:
            self.gameRoot.level.world.setFlag(
                QtWidgets.QGraphicsItem.ItemIsMovable, False)
            self.isMovable = False
        else:
            self.gameRoot.level.world.setFlag(
                QtWidgets.QGraphicsItem.ItemIsMovable, True)
            self.isMovable = True

    def updateItemsPos(self):
        self.floor_rect.setRect(self.level.world.pos().x() + self.tr.m31(),
                                self.level.world.pos().y() + self.tr.m32(),
                                self.level.world.floor.rect().width() - 2,
                                self.level.world.floor.rect().height() - 2)
        self.level.units.setPos(self.level.world.pos())
        self.level.gameVision.setPos(self.level.world.pos())
        self.level.middleLayer.setPos(self.level.world.pos())

    def mouseMoveEvent(self, e):
        if self.l_mouse:
            self.mapContains(self.frame_rect, self.level.world)
            self.updateItemsPos()
        pass

    def mapContains(self, frame_rect, world):
        mx1, my1, mx2, my2 = self.getItemCoords(world)
        wx1, wy1, wx2, wy2 = frame_rect.getCoords()
        if mx1 < wx1:
            self.setItemPos(world, wx1, my1)

        if my1 < wy1:
            self.setItemPos(world, mx1, wy1)

        if mx2 > wx2:
            self.setItemPos(world, wx2 - world.boundingRect().width(), my1)

        if my2 > wy2:
            self.setItemPos(world, mx1, wy2 - world.boundingRect().height())

        if mx1 < wx1 and my1 < wy1:
            self.setItemPos(world, wx1, wy1)

        if mx1 < wx1 and my2 > wy2:
            self.setItemPos(world, wx1, wy2 - world.boundingRect().height())

        if mx2 > wx2 and my2 > wy2:
            self.setItemPos(world, wx2 -
                            world.boundingRect().width(), wy2 -
                            world.boundingRect().height())

        if mx2 > wx2 and my1 < wy1:
            self.setItemPos(world, wx2 - world.boundingRect().width(), wy1)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self.l_mouse = True
        pass

    def mouseReleaseEvent(self, e):
        self.l_mouse = False
        pass

    def wheelEvent(self, e=None):
        self.update_frame_rect()
        # self.updateSupportField()
        # self.updateGameField()
        # self.updateScreenField()
        pass

    def update_frame_rect(self):
        tr = self.gameRoot.view.viewportTransform()

        w_world = self.level.world.floor.boundingRect().width()
        h_world = self.level.world.floor.boundingRect().height()
        map_w = w_world * tr.m11()
        map_h = h_world * tr.m22()
        scr_w = self.scr_w / tr.m11()
        scr_h = self.scr_h / tr.m22()
        scr_pos = self.gameRoot.view.mapToScene(0, 0)
        off = self.off / tr.m22()
        r = self.gameRoot.view.mapToScene(self.off, self.off)

        if map_w > self.scr_w:
            rect_w = fabs(scr_w - w_world * 2) + off * 2
            rect_x = - w_world + scr_w - off + scr_pos.x()
        else:
            rect_w = scr_w - off * 2
            rect_x = r.x()
        if map_h > self.scr_h:
            rect_h = fabs(scr_h - h_world * 2) + off * 2
            rect_y = - h_world + scr_h - off + scr_pos.y()
        else:
            rect_h = scr_h - off * 2
            rect_y = r.y()

        self.frame_rect.setRect(rect_x, rect_y, rect_w, rect_h)
        # debugLayer
        # self.level.debugLayer.frame_rect.setRect(self.frame_rect)

    def resized(self):
        self.scr_w = self.cfg.dev_size[0]
        self.scr_h = self.cfg.dev_size[1]
        if self.level is not None:
            self.initLevel(self.level)
            self.update_frame_rect()
        # self.updateGameField()
        # self.updateSupportField()
        # self.updateScreenField()

    def rectHitGroupItem(self, item):
        x = item.pos().x() + item.parentItem().pos().x() + \
            item.parentItem().transform().m31()
        y = item.pos().y() + item.parentItem().pos().y() + \
            item.parentItem().transform().m32()
        pos = self.gameRoot.view.mapFromScene(x, y)
        size = self.gameRoot.view.transform().map(
            item.boundingRect().width(), item.boundingRect().height())
        return QtCore.QRectF(pos.x(), pos.y(), size[0], size[1])

    def rectHitItem(self, item):
        pos = self.gameRoot.view.mapFromScene(item.pos())
        size = self.gameRoot.view.transform().map(
            item.boundingRect().width(), item.boundingRect().height())
        return QtCore.QRectF(pos.x(), pos.y(), size[0], size[1])

    def groupToScene(self, item):
        x = item.pos().x() + item.parentItem().pos().x() + \
            item.parentItem().transform().m31()
        y = item.pos().y() + item.parentItem().pos().y() + \
            item.parentItem().transform().m32()
        return x, y
