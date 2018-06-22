from mechanics.flexi_targeting.active.Active import Active
from mechanics.flexi_targeting.cost.Cost import Cost
from mechanics.flexi_targeting.active.user_targeting.UserTargeting import UserTargetingType
from content.events.SingleAttackEvent import attack_unit_event, attack_cell_event

std_attack_cost = Cost(1, 0)

attack_unit_active = Active(std_attack_cost,[attack_unit_event], UserTargetingType.TARGET_UNIT)
attack_cell_active = Active(std_attack_cost,[attack_cell_event], UserTargetingType.TARGET_CELL)



