from mechanics.abstract.active.Active import Active
from mechanics.abstract.event.events.SingleAttackEvent import attack_unit_event, attack_cell_event
from mechanics.abstract.cost.Cost import Cost
from mechanics.abstract.active.user_targeting.UserTargeting import UserTargetingType

std_attack_cost = Cost(1, 0)

attack_unit_active = Active(std_attack_cost,[attack_unit_event], UserTargetingType.TARGET_UNIT)
attack_cell_active = Active(std_attack_cost,[attack_cell_event], UserTargetingType.TARGET_CELL)



