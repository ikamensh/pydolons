from PySide2 import QtCore,  QtWidgets



class Actives(QtCore.QObject):
    setTargets = QtCore.Signal(list)
    def __init__(self, page, parent = None):
        super(Actives, self).__init__(parent)
        self.page = page
        self.hero = None
        self.names = None
        self.w = 400
        self.h = 96
        self.icon_size = (96, 64)
        self.frame_size = (384, 256)
        self.setNames()


        pass

    def setNames(self):
        self.names = ['run',
                      'back',
                      'atack',
                      'block',
                      'hide']
        for i in range(6, 25, 1):
            self.names.append('active_' + str(i))

    def getQss(self):
        res = 'background-color:black;' \
              'color:white;' \

        return res

    def setUp(self):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.layout = QtWidgets.QGridLayout()

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setStyleSheet(self.getQss())
        self.scrollArea.setMinimumSize(self.w, self.h)
        self.scrollArea.setFixedSize(self.w, self.h)
        self.scrollArea.setSizePolicy(sizePolicy)
        self.mwiget = QtWidgets.QWidget()
        self.mwiget.setMinimumSize(self.frame_size[0], self.frame_size[1])
        self.mwiget.setLayout(self.layout)
        self.scrollArea.setWidget(self.mwiget)
        m = 0
        self.hero = self.page.gameRoot.game.the_hero
        l = len(self.hero.actives)
        actives = list(self.hero.actives)
        size = self.getSize(l)
        # for active in self.hero.actives:
        for i in range(size[0]):
            for j in range(size[1]):
                active = actives[m]
                widget = QtWidgets.QPushButton(active.name)
                widget.setProperty('status', active.owner_can_afford_activation())
                widget.setProperty('active', active)
                # print(active.owner_can_afford_activation())
                widget.setMinimumSize(self.icon_size[0], self.icon_size[1])
                widget.setFixedSize(self.icon_size[0], self.icon_size[1])
                widget.setSizePolicy(sizePolicy)
                widget.setStyleSheet('QPushButton[status = "true"]{'\
                                     'background-color:green;}'\
                                     'QPushButton[status = "false"]{'\
                                     'background-color:gray;}'\
                                     'QPushButton:pressed {'\
                'background-color: white;'\
                'color:black}')
                widget.pressed.connect(self.selectActive)
                self.layout.addWidget(widget, i, j)
                m += 1
                if m == l:
                    break
        # self.scrollArea.move(200, 200)

    def updatePos(self, size):
        self.x = size[0] / 2 - self.w /2
        self.y = size[1] - self.h - 5
        self.scrollArea.move(self.x , self.y )

    def selectActive(self):
        active = self.mwiget.focusWidget().property('active')
        targets = self.page.gameRoot.game.get_possible_targets(active)
        if not targets is None:
            if targets:
                self.setTargets.emit(targets)
            # for target in targets:
            #     print(type(target))

    def getSize(self, l):
        n = 3
        if l % n != 0:
            return (l//n + 1, n)
        else:
            return (l//n, n)
