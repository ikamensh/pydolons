from mechanics.conditions import ActiveCondition
from cntent.monsters.tel_razi.callbacks import stun_bolt
from mechanics.actives import Active, ActiveTags
from mechanics.actives import Cost
from game_objects.battlefield_objects import BattlefieldObject


from cntent.monsters.tel_razi.callbacks import give_charges_callback
from cntent.actives.conditions.conditions import proximity_condition, within_angle


tel_razi_electrify = Active(BattlefieldObject,
                            [proximity_condition(2), within_angle(89)],
                            Cost(stamina=1, mana=10),
                            game=None,
                            callbacks=[give_charges_callback(3)],
                            tags=[ActiveTags.ATTACK, ActiveTags.RESTORATION],
                            name="Electify",
                            cooldown=5)


no_direct_activation_cond = ActiveCondition(
    "No direct activation",
    lambda a,
    t: a.owner.readiness < 1,
    "This ability can't be activated on the owners turn.")


sentinel_shot = Active(
    BattlefieldObject, [
        proximity_condition(3), within_angle(130), no_direct_activation_cond], Cost(
            stamina=1, mana=20), game=None, callbacks=[
                stun_bolt(
                    40, 0.2)], tags=[
                        ActiveTags.ATTACK, ActiveTags.RANGED], name="Electify", cooldown=4)
