from mechanics.events import Trigger
from mechanics.events import ActiveEvent

CHARGES_FIELD = "n_charges_left"

def charge_drop_callback(t:Trigger,e:ActiveEvent):
    charges_cost = e.active.cost.readiness + e.active.cost.stamina
    charges_left = getattr(t, CHARGES_FIELD)
    charges_left -= charges_cost
    charges_left = max(0, charges_left)
    if charges_left == 0:
        e.active.owner.disabled = True

    # TODO disables as property (charges)

    setattr(t, CHARGES_FIELD, charges_left)


def charge_drop_trigger(unit, max_charges):
    trig = Trigger(ActiveEvent,
            platform=unit.game.events_platform,
            conditions={lambda t, e : e.active.owner.uid == unit.uid},
            callbacks=[charge_drop_callback])


    setattr(trig, CHARGES_FIELD, max_charges)

    return trig

