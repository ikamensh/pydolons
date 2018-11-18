from mechanics.events.src.Trigger import Trigger
from mechanics.events import UnitDiedEvent
from mechanics.fractions import Fractions

from my_utils.utils import tractable_value

def compute_exp_gain(hero, monster):
    factor = (monster.xp / hero.xp) ** (4/5)
    std_amount = monster.xp ** (7/10) // 25
    return tractable_value(std_amount * factor + 0.5, digits=3)


def condition(t,e):
    if not e.killer:
        return False

    return \
        e.game.fractions[e.unit] is Fractions.ENEMY and \
        e.game.fractions[e.killer] is Fractions.PLAYER

def grant_xp_callback(t, e):
    e.killer.xp += compute_exp_gain(e.killer, e.unit)


def exp_rule(game):
    return Trigger(UnitDiedEvent,
                   platform=game.events_platform,
                   conditions={condition},
                   callbacks=[grant_xp_callback])



if __name__ == "__main__":
    from collections import namedtuple
    dummy_unit = namedtuple("unit", "xp")

    for hero_xp in [500, 2500, 12500, 50000, 1e6]:
        for monster_xp in [500, 2500, 12500, 50000, 1e6]:
            print(f"{hero_xp} | {monster_xp} | {compute_exp_gain(dummy_unit(hero_xp), dummy_unit(monster_xp))}")