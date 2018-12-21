from __future__ import annotations
import GameLog

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


class GolemCharge:
    """
    Limit the charge to max, print it
    """

    def __get__(self, golem: Golem, _):
        return golem._golem_charge

    def __set__(self, golem: Golem, value):
        old_value = golem.golem_charge
        golem._golem_charge = max(0, min(value, golem.golem_max_charge))
        delta = value - old_value
        if delta > 0:
            print( f"{golem} gains {delta :g} charge; it has {golem.golem_charge:g} charge now.")
        else:
            print( f"{golem} loses {abs(delta) :g} charge; it has {golem.golem_charge:g} charge now.")






from game_objects.battlefield_objects import Unit
class Golem(Unit):
    disabled = GolemDisabled()
    golem_charge = GolemCharge()

    @property
    def utility_factor(self):
        return self.golem_charge

    def __init__(self):
        raise NotImplemented
        self._golem_charge = None
        self.golem_max_charge = None
        self.usual_disabled = None

    @staticmethod
    def golemize(unit, max_charges):
        old_value = unit.disabled
        unit.__class__ = Golem
        unit.usual_disabled = old_value
        unit._golem_charge = max_charges
        unit.golem_max_charge = max_charges