from PySide2 import QtWidgets, QtCore, QtGui


class GameVision(QtWidgets.QGraphicsItemGroup):
    """docs GameVision"""

    def __init__(self, level):
        super(GameVision, self).__init__()
        self.level = level
        self.bf_w = self.level.gameRoot.game.bf.w
        self.bf_h = self.level.gameRoot.game.bf.h
        self.cell_w = self.level.gameRoot.cfg.getSize(103001001)[0]
        self.cell_h = self.level.gameRoot.cfg.getSize(103001001)[1]
        self.cfg = level.gameRoot.cfg
        self.game = level.gameRoot.game
        self.polyGray = self.getMainPoly()
        self.polyDark = self.getMainPoly()
        self.cur_cells = None
        self.createPoly()

    def getMainPoly(self):
        poly = QtGui.QPolygonF()
        poly.append(QtCore.QPoint(0, 0))
        poly.append(QtCore.QPoint(self.bf_w * self.cell_w, 0))
        poly.append(
            QtCore.QPoint(
                self.bf_w *
                self.cell_w,
                self.bf_h *
                self.cell_h))
        poly.append(QtCore.QPoint(0, self.bf_h * self.cell_h))
        return poly

    def setSeenCells(self, cells):
        self.cur_cells = cells
        self.updatePoly()

    def createPoly(self):
        # grad = QtGui.QRadialGradient()
        # grad.setRadius(1000)
        # grad.setFocalPoint((self.w/2) * 128,  (self.h/2) * 128)
        # grad.setCenter((self.w/2) * 128,  (self.h/2) * 128)
        # grad.setColorAt(0, QtGui.QColor.fromRgbF(0, 0, 0, 0))
        # grad.setColorAt(1, QtGui.QColor.fromRgbF(0, 0, 0, 1))
        # gBrush = QtGui.QBrush(grad)
        # # gBrush.setStyle(QtCore.Qt.RadialGradientPattern)

        pen = QtGui.QPen()
        pen.setBrush(QtCore.Qt.NoBrush)

        self.shadowGray = QtWidgets.QGraphicsPolygonItem()
        self.shadowGray.setBrush(QtCore.Qt.black)
        self.shadowGray.setPen(pen)
        self.shadowGray.setOpacity(0.6)
        self.shadowGray.setPolygon(self.polyGray)
        self.addToGroup(self.shadowGray)

        self.shadowDark = QtWidgets.QGraphicsPolygonItem()
        self.shadowDark.setBrush(QtCore.Qt.black)
        self.shadowDark.setOpacity(0.8)
        self.shadowDark.setPen(pen)
        self.shadowDark.setPolygon(self.polyDark)
        self.addToGroup(self.shadowDark)

    def updatePoly(self):
        painPath = self.getPainterPath(self.cur_cells)
        self.shadowGray.setPolygon(
            self.polyGray.subtracted(
                painPath.toFillPolygon()))
        self.polyDark = self.polyDark.subtracted(painPath.toFillPolygon())
        self.shadowDark.setPolygon(self.polyDark)

    def getPainterPath(self, cells):
        painPath = QtGui.QPainterPath()
        for cell in cells:
            painPath.addRect(
                cell.x * self.cell_w,
                cell.y * self.cell_h,
                self.cell_w,
                self.cell_h)
        return painPath
