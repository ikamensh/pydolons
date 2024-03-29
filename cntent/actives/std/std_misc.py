from mechanics.actives import Active, ActiveTags
from mechanics.actives import Cost

from cntent.actives.std.callbacks.callbacks_misc import onguard_callback, rest_callback




wait_active = Active(None,
                            [],
                            Cost(readiness=0.15),
                            callbacks=[],
                            tags=[ActiveTags.WAIT],
                            name="Wait")

onguard_active = Active(None,
                            [],
                            Cost(readiness=0.4),
                            callbacks=[onguard_callback],
                            tags=[ActiveTags.DEFEND],
                            name="Prepare to defend")

fixed_rest_cost = lambda self: Cost(readiness=1) * ( self.owner.initiative / 10)

rest_active = Active(None,
                     [],
                     fixed_rest_cost,
                     callbacks=[rest_callback],
                     tags=[ActiveTags.RESTORATION],
                     name="Rest")






