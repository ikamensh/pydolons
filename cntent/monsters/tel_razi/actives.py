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







