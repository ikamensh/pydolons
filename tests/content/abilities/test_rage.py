from cntent.abilities.battle_rage import battle_rage


from mechanics.damage import DamageTypes, Damage

from mechanics.events import DamageEvent



def test_rage(game, hero, pirate):

    hero.add_ability( battle_rage(1)() )

    str_before = hero.str
    hpmax_before = hero.max_health
    ini_before = hero.initiative
    DamageEvent(damage=Damage(100, DamageTypes.CRUSH), target=hero, source=pirate)

    assert str_before < hero.str
    assert hpmax_before < hero.max_health
    assert ini_before < hero.initiative

def test_rage_expires(game, hero, pirate):

    hero.add_ability( battle_rage(1)() )

    str_before = hero.str
    hpmax_before = hero.max_health
    ini_before = hero.initiative
    DamageEvent(damage=Damage(100, DamageTypes.CRUSH), target=hero, source=pirate)

    game.turns_manager.pass_time(10)

    assert str_before == hero.str
    assert hpmax_before == hero.max_health
    assert ini_before == hero.initiative


def test_stacks(game, hero, pirate):

    hero.add_ability( battle_rage(1)() )


    DamageEvent(damage=Damage(100, DamageTypes.CRUSH), target=hero, source=pirate)

    str_before = hero.str
    hpmax_before = hero.max_health
    ini_before = hero.initiative

    DamageEvent(damage=Damage(100, DamageTypes.CRUSH), target=hero, source=pirate)

    assert str_before < hero.str
    assert hpmax_before < hero.max_health
    assert ini_before < hero.initiative













