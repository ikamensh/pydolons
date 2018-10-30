from __future__ import annotations
from mechanics.combat import Attack
from mechanics.events import MovementEvent, TurnEvent
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from battlefield import Cell
    from mechanics.actives import Active
    from game_objects.battlefield_objects import Unit



def attack_callback(active  :Active, target :Unit):
    Attack.attack(source=active.owner, target=target)

def attack_on_cell_callback(active  :Active, target  :Cell):

    units_on_target_cell = active.game.get_units_at(target)
    if units_on_target_cell:
        chosen_target = active.game.random.choice(units_on_target_cell)
        Attack.attack(source=active.owner, target=chosen_target)

def move_on_target_cell(active: Active, target: Cell):
    MovementEvent(active.owner, target)

def turn_ccw_callback(active: Active, _):
    TurnEvent(active.owner, ccw=True)

def turn_cw_callback(active: Active, _):
    TurnEvent(active.owner, ccw=False)
