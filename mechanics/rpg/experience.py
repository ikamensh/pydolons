from mechanics.events.src.Trigger import Trigger
from mechanics.events import UnitDiedEvent
from mechanics.fractions import Fractions
import my_context


def compute_exp_gain(hero, monster):
    factor = (monster.xp / hero.xp) ** (4/5)
    std_amount = monster.xp ** (7/10) // 25
    return int(std_amount * factor + 0.5)


def condition(t,e):
    if not e.killer:
        return False

    return \
        my_context.the_game.fractions[e.unit] is Fractions.ENEMY and \
        my_context.the_game.fractions[e.killer] is Fractions.PLAYER

def grant_xp_callback(t, e):
    e.killer.xp += compute_exp_gain(e.killer, e.unit)


def exp_rule():
    return Trigger(UnitDiedEvent,
                   conditions={condition},
                   callbacks=[grant_xp_callback])



if __name__ == "__main__":
    from collections import namedtuple
    dummy_unit = namedtuple("unit", "xp")

    for hero_xp in [500, 2500, 12500, 50000, 1e6]:
        for monster_xp in [500, 2500, 12500, 50000, 1e6]:
            print(f"{hero_xp} | {monster_xp} | {compute_exp_gain(dummy_unit(hero_xp), dummy_unit(monster_xp))}")