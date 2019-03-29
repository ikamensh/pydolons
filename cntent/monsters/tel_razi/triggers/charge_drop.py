from __future__ import annotations
from mechanics.events import Trigger
from mechanics.events import ActiveEvent
from cntent.monsters.tel_razi import Golem


def charge_drop_callback(t: Trigger, e: ActiveEvent):
    unit: Golem = e.active.owner
    charges_cost = e.active.cost.readiness + e.active.cost.stamina
    unit.golem_charge -= charges_cost


def charge_drop_trigger(unit, max_charges):
    trig = Trigger(ActiveEvent,
                   platform=unit.game.events_platform,
                   conditions={lambda t, e: e.active.owner.uid == unit.uid},
                   callbacks=[charge_drop_callback])

    Golem.golemize(unit, max_charges)

    return trig
