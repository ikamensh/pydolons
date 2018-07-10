from mechanics.flexi_targeting import Active
from mechanics.flexi_targeting import Cost
from content.packs.SingleAttackPack import attack_unit_pack, attack_cell_pack

std_attack_cost = Cost(1, 0)

attack_unit_active = Active(std_attack_cost, attack_unit_pack)
attack_cell_active = Active(std_attack_cost, attack_cell_pack)



