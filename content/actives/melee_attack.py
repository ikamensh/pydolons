from mechanics.flexi_targeting import Active
from mechanics.flexi_targeting import Cost
from mechanics.flexi_targeting import UserTargetingType
from content.packs.SingleAttackPack import attack_unit_event, attack_cell_event

std_attack_cost = Cost(1, 0)

attack_unit_active = Active(std_attack_cost,[attack_unit_event], UserTargetingType.TARGET_UNIT)
attack_cell_active = Active(std_attack_cost,[attack_cell_event], UserTargetingType.TARGET_CELL)



