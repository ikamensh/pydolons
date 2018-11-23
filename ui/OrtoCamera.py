import sys


from PySide2 import QtCore, QtGui, QtWidgets

from ui.GameRootNode import GameRootNode

from ui.GameAnimation import Animations


from ui.GameView import GameView


from datetime import datetime


class Camera(QtCore.QObject):
    def __init__(self, cfg):
        super(Camera, self).__init__()
        self.cfg = cfg
        self.tr = QtGui.QTransform()
        # self.tr.scale(2 / 1.05, 2 / 1.05)
        origin_x = self.cfg.dev_size[0] / 2
        origin_y = self.cfg.dev_size[1] / 2
        self.tr.translate(origin_x, origin_y)
        print(self.tr)
        # self.setOrigin(100, 200, self.tr)

    def setOrigin(self, x, y, tr:QtGui.QTransform):
        m11 = tr.m11()
        m12 = tr.m12()
        # m13 = tr.m13()
        m13 = y
        m21 = tr.m21()
        m22 = tr.m22()
        # m23 = tr.m23()
        m23 = x
        m31 = tr.m31()
        m32 = tr.m32()
        m33 = tr.m33()
        tr.setMatrix(m11, m12, m13, m21, m22, m23, m31, m32, m33)

    def keyPressEvent(self, e):
        dx = self.world.hero.rect().width()
        dy = self.world.hero.rect().height()
        if e.key() == QtCore.Qt.Key_Up:
            self.translate(0, dy)
        if e.key() == QtCore.Qt.Key_Down:
            self.translate(0, -dy)
        if e.key() == QtCore.Qt.Key_Left:
            self.translate(dx, 0)
        if e.key() == QtCore.Qt.Key_Right:
            self.translate(-dx, 0)
        pass

    def translate(self, dx, dy):
        # self.tr.translate(dx, dy)
        self.world.setTransform(self.tr)
        self.world.moveBy(dx * self.tr.m11(), dy * self.tr.m22())
        self.world.hero.moveBy(-dx, -dy)
        x = self.world.hero.boundingRect().x() + self.world.hero.x()
        y = self.world.hero.boundingRect().y() + self.world.hero.y()
        self.w_rect = self.getWorldRect()
        # self.g_rect =  self.getGroundRect()=
        self.g_rect = QtCore.QRectF(- self.tr.m31() + 128, - self.tr.m32() + 128, -self.world.boundingRect().width() + self.cfg.dev_size[0] - 256, -self.world.boundingRect().height() + self.cfg.dev_size[1] - 256)
        print('w_rect:', self.w_rect)
        print('g_rect:', self.g_rect.getCoords())

        xw = self.world.boundingRect().x() + self.world.x()
        yw = self.world.boundingRect().y() + self.world.y()

        print('xw, yw', xw, yw)

        if self.w_rect.contains(x, y):

            if self.g_rect.contains(xw, yw):
                pass
                print('g:', True)
            else:
                print('g:', False)
                self.world.moveBy(-dx, -dy)
            print('w:',True)
        else:
            self.world.moveBy(-dx, -dy)
            self.world.hero.moveBy(dx, dy)
            print(False)

    def getWorldRect(self):
        w, h = 128 * self.tr.m11(), 128 * self.tr.m22()
        w_rect: QtCore.QRectF = self.world.boundingRect()
        rect = QtCore.QRectF(w_rect.x(), w_rect.y(), w_rect.width() - w, w_rect.height() - h)
        print(rect)
        return rect

    def getGroundRect(self):
        rect:QtCore.QRectF = self.world.boundingRect()
        return QtCore.QRectF(-rect.width(), -rect.height(), rect.width() * 2, rect.height() * 2)


    def getWorldCoords(self):
        return self.tr.map(self.world.ground.pos())

    def moveHero(self, dx, dy):
        # print(self.world.hero.pos())
        print(self.world.hero.mapFromParent(self.world.hero.pos()))
        print(self.tr.map(self.world.hero.pos().x(), self.world.hero.pos().y()))
        print(self.tr.map(self.world.mapFromScene(self.world.hero.pos())))
        self.world.hero.setPos(self.world.hero.pos().x() - dx, self.world.hero.pos().y() - dy)

    def mouseReleaseEvent(self, e):
        pass

    def mouseMoveEvent(self, e):
        pass

    def mousePressEvent(self, e):
        pass

    def wheelEvent(self, e):
        """ Метод перехватывает событие мышки скролл, скролл больше 0 зумм +,
        скролл меньше нуля зумм -
        """
        if e.delta() > 0.0:
            self.zoomIn()
        elif e.delta() < 0.0:
            self.zoomOut()
        pass

    def zoomIn(self):
        self.tr.scale(1.05, 1.05)
        self.world.setTransform(self.tr)


    def zoomOut(self):
        self.tr.scale(1/1.05, 1/1.05)
        self.world.setTransform(self.tr)




class TheUI(QtWidgets.QWidget):
    view = None
    singleton = None

    def __init__(self):
        super().__init__()

        cursor = QtGui.QCursor(QtGui.QPixmap('resources/assets/ui/cursor.png'))
        self.setCursor(cursor)

        self.gameRoot: GameRootNode = GameRootNode()
        self.gameRoot.ui = self

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.view = GameView(self)
        self.gameRoot.setView(self.view)

        self.gameconfig = self.view.gameconfig
        self.gameconfig.animations = Animations()
        self.gameRoot.setGameConfig(self.view.gameconfig)
        self.layout.addWidget(self.view)
        self.layout.setMargin(2)

        self.scene = QtWidgets.QGraphicsScene(0, 0, 500, 500)
        self.gameRoot.setScene(self.scene)
        self.scene.setFocus(focusReason=QtCore.Qt.OtherFocusReason)
        self.scene.setBackgroundBrush(QtGui.QBrush(self.gameconfig.getPicFile('dungeon.jpg')))

        self.camera = Camera(self.gameconfig)
        self.view.controller = self.camera
        self.setWorld()
        self.setLabels()
        self.view.setScene(self.scene)

        self.showMaximized()
        print('cfg ===> init TheUI', datetime.now())


    def changeTo(self):
        self.scene.update(-self.gameconfig.ava_ha_size[0],
                          -self.gameconfig.ava_ha_size[1],
                          self.gameconfig.ava_size[0],
                          self.gameconfig.ava_size[1])


    def setWorld(self):
        self.world = QtWidgets.QGraphicsItemGroup()
        w, h = 32, 32
        ground_pix = self.gameRoot.cfg.getPicFile('floor.png', 102001001)

        ground_w = ground_pix.width()
        ground_h = ground_pix.height()

        self.ground = QtWidgets.QGraphicsRectItem()
        self.ground.setBrush(QtGui.QBrush(ground_pix))
        self.ground.setRect(-ground_w *w/2, -ground_h * h/2, ground_w * w, ground_h * h)

        self.hero = QtWidgets.QGraphicsRectItem()
        self.hero.setBrush(QtCore.Qt.red)
        self.hero.setRect(-ground_w * 4, -ground_h * 2, ground_w , ground_h )


        self.world.addToGroup(self.ground)
        self.world.addToGroup(self.hero)
        self.world.hero = self.hero
        self.world.ground =self.ground
        self.scene.addItem(self.world)
        self.camera.world = self.world

    def setLabels(self):
        self.widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        wPosLab = QtWidgets.QLabel('(0.0, 0.0)', self.widget)
        wPosLab.setFixedWidth(500)
        layout.addWidget(wPosLab, 0, 1)
        self.widget.wPosLab = wPosLab
        self.scene.addWidget(self.widget)
        self.camera.widget = self.widget



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TheUI()
    sys.exit(app.exec_())
