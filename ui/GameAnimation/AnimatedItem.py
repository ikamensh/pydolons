from ui.gamecore.GameObject import GameObject
from PySide2 import QtCore
from random import randint


class AnimatedItem(QtCore.QObject, GameObject):
    animationFinished = QtCore.Signal()

    def __init__(self, *arg, gameconfig, parent = None):
        QtCore.QObject.__init__(self, parent)
        GameObject.__init__(self, *arg)
        self.cfg = gameconfig
        self.setUpTimer()
        self.picmaps = []
        self.n_frames = 0
        self.current_index = 0
        self.mode = False

    def setPics(self, name):
        """ for animation file name template
            file_name = pic_0.png
            name = 'pic'
            index = '0'
            type = '.png'
        """
        i = 0
        while True:
            pic = self.cfg.pix_maps.get(name + '_' + str(i) + '.png')
            i += 1
            if pic is None:
                break
            else:
                self.picmaps.append(pic)

    def setUpTimer(self):
        self.m_timer = QtCore.QTimer()
        self.m_timer.timeout.connect(self.on_timerTick)

    def animation(self, framerate=25, mode=False, random_index=True):
        self.mode = mode
        self.m_timer.stop()
        self.n_frames = len(self.picmaps)
        if random_index:
            self.current_index = randint(0, self.n_frames - 1)
        else:
            self.current_index = 0
        self.setPixmap(self.picmaps[self.current_index])
        if framerate > 0 :
            self.m_timer.setInterval(1000/framerate)
            self.m_timer.start()

    def on_timerTick(self):
        self.current_index += 1
        if self.mode:
            if self.current_index >= self.n_frames:
                self.current_index = 0
            self.setPixmap(self.picmaps[self.current_index])
        else:
            if self.current_index >= self.n_frames:
                self.m_timer.stop()
                self.hide()
                self.animationFinished.emit()
            else:
                self.setPixmap(self.picmaps[self.current_index])




