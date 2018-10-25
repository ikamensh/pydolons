import sys
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, \
    QVBoxLayout, QFormLayout, QComboBox, QLineEdit, QLabel
from PySide2 import QtWidgets
from PySide2 import QtGui
from cntent.dungeons.small_orc_cave import small_orc_cave
from DreamGame import DreamGame

from ui.GameConfiguration import GameConfiguration


# Every Qt application must have one and only one QApplication object;
# it receives the command line arguments passed to the script, as they
# can be used to customize the application's appearance and behavior
qt_app = QApplication(sys.argv)

gc = GameConfiguration()

class DungeonWidget(QWidget):
    def __init__(self, dungeon, parent = None):
        QWidget.__init__(self, parent)
        self.dungeon = dungeon

        # Create the form layout that manages the labeled controls
        self.form_layout = QFormLayout()

        self.icon = QtWidgets.QGraphicsPixmapItem()

        pixmap = QtGui.QPixmap(dungeon.icon)
        self.icon.setPixmap()

        locs = dungeon.unit_locations(DreamGame())

        self.n_units_label = QLabel(f'{len(locs.keys())}', self)
        self.form_layout.addRow('Units in the dungeon:', self.n_units_label)

        self.max_xp_label = QLabel(f'{max([u.xp for u in locs.keys()])}', self)
        self.form_layout.addRow('Strongest enemy XP: ', self.max_xp_label)

        self.setLayout(self.form_layout)

    def run(self):
        # Show the form
        self.show()
        # Run the qt application
        qt_app.exec_()






# Create an instance of the application window and run it
app = DungeonWidget(small_orc_cave)
app.run()