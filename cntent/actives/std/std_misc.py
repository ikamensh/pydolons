from mechanics.actives import Active, ActiveTags
from mechanics.actives import Cost

from cntent.actives.std.callbacks.callbacks_misc import onguard_callback, rest_callback


wait_active = Active(None,
                     [],
                     Cost(readiness=0.15),
                     game=None,
                     callbacks=[],
                     tags=[ActiveTags.WAIT],
                     name="Wait")

onguard_active = Active(None,
                        [],
                        Cost(readiness=0.4),
                        game=None,
                        callbacks=[onguard_callback],
                        tags=[ActiveTags.DEFEND],
                        name="Prepare to defend")


def fixed_rest_cost(self): return Cost(
    readiness=1) * (self.owner.initiative / 10)


rest_active = Active(None,
                     [],
                     fixed_rest_cost,
                     game=None,
                     callbacks=[rest_callback],
                     tags=[ActiveTags.RESTORATION],
                     name="Rest")
