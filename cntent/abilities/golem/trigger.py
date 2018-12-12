from __future__ import annotations
from mechanics.events import Trigger
from mechanics.events import ActiveEvent

class GolemDisabled:
    """
    If a golem has 0 or less charges, he is always disabled.
    Otherwise normal rules apply.
    """
    old_value_key = "_disabled"

    def __get__(self, golem: Golem, _):
        if golem.golem_charge <= 0:
            return True
        else:
            return golem.usual_disabled

    def __set__(self, golem: Golem, value):
        golem.usual_disabled = value


from game_objects.battlefield_objects import Unit
class Golem(Unit):
    disabled = GolemDisabled()

    def __init__(self):
        raise NotImplemented
        self.golem_charge = None
        self.usual_disabled = None

    @staticmethod
    def make_golem(unit, max_charges):
        old_value = unit.disabled
        unit.__class__ = Golem
        unit.usual_disabled = old_value
        unit.golem_charge = max_charges


def charge_drop_callback(t:Trigger,e:ActiveEvent):
    unit: Golem = e.active.owner
    charges_cost = e.active.cost.readiness + e.active.cost.stamina
    unit.golem_charge -= charges_cost


def charge_drop_trigger(unit, max_charges):
    trig = Trigger(ActiveEvent,
            platform=unit.game.events_platform,
            conditions={lambda t, e : e.active.owner.uid == unit.uid},
            callbacks=[charge_drop_callback])


    Golem.make_golem(unit, max_charges)


    return trig

