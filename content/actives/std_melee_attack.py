from mechanics.actives import Active, ActiveTags
from mechanics.actives import Cost
from game_objects.battlefield_objects import BattlefieldObject
from battlefield import Cell


from content.actives.callbacks import attack_callback, attack_on_cell_callback
from content.actives.conditions import proximity_condition, within_angle


std_attack_cost = Cost(stamina=1)


attack_unit_active = Active(BattlefieldObject,
                            [proximity_condition(1.5), within_angle(45)],
                            std_attack_cost,
                            [attack_callback],
                            [ActiveTags.ATTACK])

attack_cell_active = Active(Cell,
                            [proximity_condition(1.5), within_angle(45)],
                            std_attack_cost,
                            [attack_on_cell_callback],
                            [ActiveTags.ATTACK])

std_attacks = [attack_unit_active]





