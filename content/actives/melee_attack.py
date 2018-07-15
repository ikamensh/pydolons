from mechanics.flexi_targeting import Active, CellTargeting, SingleUnitTargeting
from mechanics.flexi_targeting import Cost
from mechanics.combat import Attack

import my_globals


std_attack_cost = Cost(1, 0)

def attack_direct_callback(active  :Active, targeting  :SingleUnitTargeting):
    Attack.attack(source=active.owner, target=targeting.unit)

def attack_on_cell_callback(active  :Active, targeting  :CellTargeting):
    unit_on_target_cell = my_globals.the_game.get_unit_at(targeting.cell)
    Attack.attack(source=active.owner, target=unit_on_target_cell)

attack_unit_active = Active(SingleUnitTargeting, std_attack_cost, [attack_direct_callback])
attack_cell_active = Active(CellTargeting, std_attack_cost, [attack_on_cell_callback])



