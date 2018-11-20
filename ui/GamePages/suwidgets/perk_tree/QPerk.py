from __future__ import annotations

from PySide2.QtWidgets import QPushButton, QWidget, QLabel, QVBoxLayout
from PySide2.QtGui import QPixmap
from PySide2 import QtCore


from character.perks import Perk, PerkTree

class QPerk(QWidget):
    def __init__(self, cfg, perk: Perk, parent):
        self.cfg = cfg
        self.perk = perk
        self.perk_tree: PerkTree = parent.tree.perk_tree
        self.group = parent
        super().__init__(parent)

        layout = QVBoxLayout()
        pixmap = QPixmap(self.cfg.getPicFile(perk.icon, 101004001))
        icon = QLabel(self)
        icon.setPixmap(pixmap)
        icon.setFixedSize(pixmap.size())
        layout.addWidget(icon)
        layout.setAlignment(icon, QtCore.Qt.AlignCenter)
        self.icon = icon
        up_button = QPushButton(self)
        up_button.clicked.connect(self.on_click)
        up_button.setText("Not initialized")
        layout.addWidget(up_button)
        self.up_button = up_button

        layout.setSizeConstraint(QVBoxLayout.SetFixedSize)
        self.setLayout(layout)

        self.border_color = {0:"white", 1:"yellow", 2:"orange", 3:"red"}
        self.match_level()

    @property
    def xp_to_levelup(self):
        return self.perk_tree.cost_to_levelup(self.perk)

    def xp_changed(self, new_xp):
        if self.perk.current_level < 3:
            if new_xp < self.xp_to_levelup:
                self.up_button.setDisabled(True)
            else:
                self.up_button.setEnabled(True)

            self.up_button.setText(self.string_cost(self.xp_to_levelup))

    @staticmethod
    def string_cost(cost):

        if cost >= 1e6:
            value = int(cost // 1000_000)
            rest = int((cost - value*1000_000) // 100_000)
            if rest != 0:
                result = f"{value}.{rest}m"
            else:
                result = f"{value}m"
        elif cost > 1000:
            value = int(cost // 1000)
            rest = int((cost - value*1000) // 100)
            if rest != 0:
                result = f"{value}.{rest}k"
            else:
                result = f"{value}k"
        else:
            result = str(cost)

        return result

    def match_level(self):
        color = self.border_color[self.perk.current_level]
        self.icon.setStyleSheet(f"border: 3px solid {color}")
        if self.perk.current_level == 3:
            self.up_button.setDisabled(True)
            self.up_button.setText("^maxed^")

    def on_click(self):
        self.perk_tree.spent_xp += self.xp_to_levelup
        self.perk.current_level += 1
        self.match_level()
        self.group.levelup()



if __name__ == "__main__":
    from character.perks.everymans_perks.group_attrib import str_perk
    from PySide2.QtWidgets import QApplication

    qt_app = QApplication()

    app = QPerk(str_perk)
    app.show()


    qt_app.exec_()