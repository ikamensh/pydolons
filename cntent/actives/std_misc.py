from mechanics.actives import Active, ActiveTags
from mechanics.actives import Cost
from game_objects.battlefield_objects import BattlefieldObject
from battlefield import Cell


from cntent.actives.callbacks_misc import onguard_callback, rest_callback




wait_active = Active(BattlefieldObject,
                            [],
                            Cost(readiness=0.15),
                            game=None,
                            callbacks=[],
                            tags=[ActiveTags.WAIT],
                            name="Standard attack")

onguard_active = Active(Cell,
                            [],
                            Cost(readiness=0.4),
                            game=None,
                            callbacks=[onguard_callback],
                            tags=[ActiveTags.DEFEND],
                            name="Attack Cell")

rest_active = Active(Cell,
                            [],
                            Cost(readiness=1),
                            game=None,
                            callbacks=[rest_callback],
                            tags=[ActiveTags.REST],
                            name="Attack Cell")

std_attacks = [attack_unit_active]





