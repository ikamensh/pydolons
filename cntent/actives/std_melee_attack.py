from mechanics.actives import Active, ActiveTags
from mechanics.actives import Cost
from game_objects.battlefield_objects import BattlefieldObject
from battlefield import Cell


from cntent.actives.callbacks import attack_callback, attack_on_cell_callback
from cntent.actives.conditions import proximity_condition, within_angle


std_attack_cost = lambda  self: Cost(stamina=1)*self.owner.get_melee_weapon().atb_factor


attack_unit_active = Active(BattlefieldObject,
                            [proximity_condition(1.5), within_angle(45)],
                            std_attack_cost,
                            game=None,
                            callbacks=[attack_callback],
                            tags=[ActiveTags.ATTACK],
                            name="Standard attack")

attack_cell_active = Active(Cell,
                            [proximity_condition(1.5), within_angle(45)],
                            std_attack_cost,
                            game=None,
                            callbacks=[attack_on_cell_callback],
                            tags=[ActiveTags.ATTACK],
                            name="Attack Cell")

std_attacks = [attack_unit_active]





