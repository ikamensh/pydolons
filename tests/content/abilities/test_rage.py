from cntent.abilities.battle_rage.ability import battle_rage


from mechanics.damage import DamageTypes, Damage

from mechanics.events import DamageEvent



def test_rage(game_hvsp, hero, pirate):

    hero.add_ability( battle_rage(1)() )

    str_before = hero.str
    hpmax_before = hero.max_health
    ini_before = hero.initiative
    DamageEvent(damage=Damage(100, DamageTypes.CRUSH), target=hero, source=pirate)

    assert str_before < hero.str
    assert hpmax_before < hero.max_health
    # assert ini_before < hero.initiative # initiative is rounded as an integer and is not guaranteed to grow

def test_rage_expires(game_hvsp, hero, pirate):

    hero.add_ability( battle_rage(1)() )

    str_before = hero.str
    hpmax_before = hero.max_health
    ini_before = hero.initiative
    DamageEvent(damage=Damage(100, DamageTypes.CRUSH), target=hero, source=pirate)

    game_hvsp.turns_manager.pass_time(10)

    assert str_before == hero.str
    assert hpmax_before == hero.max_health
    assert ini_before == hero.initiative


def test_stacks(game_hvsp, hero, pirate):

    hero.add_ability( battle_rage(1)() )


    DamageEvent(damage=Damage(100, DamageTypes.CRUSH), target=hero, source=pirate)

    str_before = hero.str
    hpmax_before = hero.max_health
    ini_before = hero.initiative

    DamageEvent(damage=Damage(100, DamageTypes.CRUSH), target=hero, source=pirate)

    assert str_before < hero.str
    assert hpmax_before < hero.max_health
    assert ini_before < hero.initiative













