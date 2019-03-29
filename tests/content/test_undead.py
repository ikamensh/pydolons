from cntent.monsters.undead import skeleton, zombie, ghost
from mechanics.events import DamageEvent
from mechanics.damage import Damage, DamageTypes


def test_undying(game_hvsp):
    z = zombie.create(game_hvsp)
    game_hvsp.add_unit(z, 6 + 6j, None)

    z.health -= 99999
    assert z.alive

    s = skeleton.create(game_hvsp)
    game_hvsp.add_unit(s, 6 + 7j, None)

    s.health -= 99999
    assert s.alive

    for _ in range(10):
        z.health -= 99999
        s.health -= 99999
    assert not z.alive
    assert not s.alive


def test_ghost(empty_game):

    g = ghost.create(empty_game)
    z = zombie.create(empty_game)

    empty_game.add_unit(g, 1 + 1j)

    empty_game.add_unit(z, 1 + 1j)

    DamageEvent(damage=Damage(1, DamageTypes.ACID), target=z, source=g)
    assert z.mana == z.max_mana  # no damage

    DamageEvent(damage=Damage(300, DamageTypes.ACID), target=z, source=g)
    assert z.mana < z.max_mana
