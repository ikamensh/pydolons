from cntent.monsters.undead import skeleton, zombie



def test_undying(game):
    z = zombie.create()
    game.add_unit(z, 6+6j, None)

    z.health -= 99999
    assert z.alive

    s = skeleton.create()
    game.add_unit(s, 6 + 7j, None)

    s.health -= 99999
    assert s.alive


    for _ in range(10):
        z.health -= 99999
        s.health -= 99999
    assert not z.alive
    assert not s.alive