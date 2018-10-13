from mechanics.combat import Attack
from mechanics.actives import Active
from mechanics.events import MovementEvent, TurnEvent
from battlefield import Cell
from game_objects.battlefield_objects import Unit



def attack_callback(active  :Active, target :Unit):
    Attack.attack(active.game, source=active.owner, target=target)

def attack_on_cell_callback(active  :Active, target  :Cell):

    unit_on_target_cell = active.game.get_unit_at(target)
    Attack.attack(active.game, source=active.owner, target=unit_on_target_cell)

def move_on_target_cell(active: Active, target: Cell):
    MovementEvent(active.game, active.owner, target)

def turn_ccw_callback(active: Active, _):
    TurnEvent(active.game, active.owner, ccw=True)

def turn_cw_callback(active: Active, _):
    TurnEvent(active.game, active.owner, ccw=False)
