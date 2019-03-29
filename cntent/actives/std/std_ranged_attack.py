from mechanics.actives import Active, ActiveTags
from mechanics.actives import Cost
from game_objects.battlefield_objects import BattlefieldObject


from cntent.actives.std.callbacks.callbacks import ranged_attack_cb
from cntent.actives.conditions.conditions import range_condition, within_angle


def std_ranged_cost(self): return Cost(stamina=1) * \
    self.owner.get_ranged_weapon().atb_factor


bow_shot_active = Active(BattlefieldObject,
                         [range_condition(2, 4), within_angle(45)],
                         std_ranged_cost,
                         game=None,
                         callbacks=[ranged_attack_cb],
                         tags=[ActiveTags.RANGED, ActiveTags.ATTACK],
                         name="Bow shot")

crossbow_shot_active = Active(BattlefieldObject,
                              [range_condition(2, 5), within_angle(45)],
                              std_ranged_cost,
                              game=None,
                              callbacks=[ranged_attack_cb],
                              tags=[ActiveTags.RANGED, ActiveTags.ATTACK],
                              name="Crossbow shot")
