from __future__ import annotations

from PySide2.QtCore import QPropertyAnimation, QParallelAnimationGroup
from ui.animation import GameVariantAnimation


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.core.levels import BaseLevel
    from ui.world.units.BasicUnit import BasicUnit
    from game_objects.battlefield_objects import Unit


DURATION_BASIC = 500
DURATION_UNIT_MOVE = 300


def create_move_animation(unit: BasicUnit, duration=DURATION_UNIT_MOVE):
    group = QParallelAnimationGroup()
    move_anim = GameVariantAnimation(unit)
    move_anim.setDuration(duration)
    visible_anim = GameVariantAnimation(unit)
    visible_anim.setDuration(duration)
    group.addAnimation(move_anim)
    group.addAnimation(visible_anim)
    return group
