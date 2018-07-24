from mechanics.actives import Active, CellTargeting, SingleUnitTargeting, ActiveTags
from mechanics.actives import Cost
from content.actives.callbacks import move_on_target_cell, turn_ccw_callback, turn_cw_callback

from content.actives.conditions import proximity_condition, within_angle, between_angles


std_attack_cost = Cost(stamina=1)




move_forward = Active(CellTargeting,
                            [proximity_condition(1), within_angle(0)],
                            Cost(stamina=1, readiness=0.3),
                            [move_on_target_cell],
                            [ActiveTags.MOVEMENT])

move_diag = Active(CellTargeting,
                            [proximity_condition(1.5), between_angles(89,91)],
                            Cost(stamina=2, readiness=0.6),
                            [move_on_target_cell],
                            [ActiveTags.MOVEMENT])

move_side = Active(CellTargeting,
                            [proximity_condition(1), between_angles(89,91)],
                            Cost(stamina=1, readiness=0.5),
                            [move_on_target_cell],
                            [ActiveTags.MOVEMENT])

move_back = Active(CellTargeting,
                            [proximity_condition(1), between_angles(180,180)],
                            Cost(stamina=1, readiness=0.6),
                            [move_on_target_cell],
                            [ActiveTags.MOVEMENT])

turn_cw = Active(None,
                 None,
                 Cost(readiness=0.1),
                 [turn_cw_callback],
                            [ActiveTags.TURNING])

turn_ccw = Active(None,
                 None,
                 Cost(readiness=0.1),
                 [turn_ccw_callback],
                            [ActiveTags.TURNING])


std_movements = [move_back, move_diag, move_forward, move_side, turn_cw, turn_ccw]
