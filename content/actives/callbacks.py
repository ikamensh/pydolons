from mechanics.combat import Attack
from mechanics.actives import Active, CellTargeting, SingleUnitTargeting
from mechanics.events import MovementEvent, TurnEvent

import my_globals

def attack_callback(active  :Active, targeting  :SingleUnitTargeting):
    Attack.attack(source=active.owner, target=targeting.unit)

def attack_on_cell_callback(active  :Active, targeting  :CellTargeting):
    unit_on_target_cell = my_globals.the_game.get_unit_at(targeting.cell)
    Attack.attack(source=active.owner, target=unit_on_target_cell)

def move_on_target_cell(active: Active, targeting: CellTargeting):
    MovementEvent(my_globals.the_game.battlefield, active.owner, targeting.cell)

def turn_ccw_callback(active: Active, _):
    TurnEvent(my_globals.the_game.battlefield, active.owner, ccw=True)

def turn_cw_callback(active: Active, _):
    TurnEvent(my_globals.the_game.battlefield, active.owner, ccw=False)
