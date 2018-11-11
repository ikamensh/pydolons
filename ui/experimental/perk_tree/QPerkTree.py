from character.perks import PerkTree
from PySide2.QtWidgets import QWidget, QVBoxLayout
from ui.experimental.perk_tree.QPerkGroup import QPerkGroup


from PySide2.QtCore import Qt

class QPerkTree(QWidget):


    def __init__(self, perk_tree: PerkTree, parent=None):
        self.perk_tree = perk_tree
        super().__init__(parent)

        layout = QVBoxLayout()

        layout.setAlignment(Qt.AlignCenter)

        self.visuals = {}
        for perk_group in perk_tree.perk_groups:
            qpg = QPerkGroup( perk_group, self )
            self.visuals[perk_group] = qpg
            layout.addWidget( qpg )
            layout.addStretch(2)

        self.setLayout(layout)

    def xp_changed(self, new_xp):
        for qpg in self.visuals.values():
            qpg.xp_changed(new_xp)

    def levelup(self):
        self.xp_changed(1e6)


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication
    from character.perks.everymans_perks.everymans_perk_tree import everymans_perks
    tree = everymans_perks()

    qt_app = QApplication()

    app = QPerkTree(tree)
    app.show()

    qt_app.exec_()