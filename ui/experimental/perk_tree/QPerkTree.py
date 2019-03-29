from __future__ import annotations

from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel
from ui.experimental.perk_tree.QPerkGroup import QPerkGroup


from PySide2.QtCore import Qt

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from character.perks import PerkGroup
    from character.perks import PerkTree
    from character.Character import Character


class QPerkTree(QWidget):

    def __init__(self, perk_tree: PerkTree, character: Character, parent=None):
        assert perk_tree in character.perk_trees

        self.perk_tree = perk_tree
        self.character = character
        super().__init__(parent)

        layout = QVBoxLayout()

        layout.setAlignment(Qt.AlignCenter)

        self.name = QLabel(perk_tree.name)
        layout.addWidget(self.name)
        self.total_spent = QLabel(str(perk_tree.spent_xp))
        layout.addWidget(self.total_spent)

        self.visuals = {}
        for perk_group in perk_tree.perk_groups:
            qpg = QPerkGroup(perk_group, self)
            self.visuals[perk_group] = qpg
            layout.addWidget(qpg)
            layout.addStretch(2)

        self.setLayout(layout)
        self.xp_changed(self.character.free_xp)

    def xp_changed(self, new_xp):
        for qpg in self.visuals.values():
            qpg.xp_changed(new_xp)

    def levelup(self):
        self.total_spent.setText(str(self.perk_tree.spent_xp))
        self.xp_changed(self.character.free_xp)


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication
    from character.Character import Character
    from cntent.base_types.demo_hero import demohero_basetype

    c = Character(demohero_basetype)
    c.unit.xp = 1e6

    tree = c.perk_trees[0]

    qt_app = QApplication()

    app = QPerkTree(tree, c)
    app.show()

    qt_app.exec_()
