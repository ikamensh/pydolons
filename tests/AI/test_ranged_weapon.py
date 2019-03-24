from cntent.monsters.tel_razi.monsters import tel_razi_scrub
from mechanics.AI import BruteAI

def test_shoots(empty_simgame, hero):
    shooter = tel_razi_scrub.create(empty_simgame)

    empty_simgame.add_unit(shooter, 2+2j, faction="Clan A", facing=1j)
    empty_simgame.add_unit(hero, 2+4j, faction="Clan B")

    ai = BruteAI(empty_simgame)
    active, target = ai.decide_step(shooter)

    print(active, target)

    assert target is hero

def test_can_shoot(empty_simgame, hero):
    assert empty_simgame.bf.game is empty_simgame
    shooter = tel_razi_scrub.create(empty_simgame)

    empty_simgame.add_unit(shooter, 2+2j, facing=1j)
    empty_simgame.add_unit(hero, 2+4j)

    from mechanics.actives import ActiveTags
    ranged_actives = [a for a in shooter.actives if ActiveTags.RANGED in a.tags]
    ranged_active = ranged_actives[0]

    assert hero in empty_simgame.get_possible_targets(ranged_active)

def test_cant_shoot_facing(empty_simgame, hero):
    shooter = tel_razi_scrub.create(empty_simgame)

    empty_simgame.add_unit(shooter, 2+2j, facing=-1j)
    empty_simgame.add_unit(hero, 2+4j)

    from mechanics.actives import ActiveTags
    ranged_actives = [a for a in shooter.actives if ActiveTags.RANGED in a.tags]
    ranged_active = ranged_actives[0]

    assert hero not in empty_simgame.get_possible_targets(ranged_active)

def test_has_shoot_active(empty_simgame):
    shooter = tel_razi_scrub.create(empty_simgame)

    empty_simgame.add_unit(shooter, 2+2j)

    from mechanics.actives import ActiveTags
    ranged_actives = [ a for a in shooter.actives if ActiveTags.RANGED in a.tags]

    assert ranged_actives



