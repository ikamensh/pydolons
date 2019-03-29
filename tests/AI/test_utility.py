from mechanics.actives import ActiveTags
from mechanics.AI.SimGame import SimGame
import pytest

utility = SimGame.unit_utility


def test_unit_util_positive(hero, pirate):
    assert utility(hero) > 0
    assert utility(pirate) > 0


def test_more_hp_is_better(minigame, hero):

    utility_initial = minigame.utility(hero.faction)
    hero.max_health += 100
    assert utility_initial < minigame.utility(hero.faction)


def test_invertion(minigame, hero):
    pirate = [unit for unit in minigame.units if unit is not hero][0]

    utility_initial = minigame.utility(pirate.faction)
    hero.max_health += 100
    assert utility_initial > minigame.utility(pirate.faction)


def test_less_hp_is_worse(minigame, hero):

    utility_initial = minigame.utility(hero.faction)
    hero.max_health -= 100
    assert utility_initial > minigame.utility(hero.faction)


def test_double_inversion(minigame, hero):

    pirate = [unit for unit in minigame.units if unit is not hero][0]
    utility_initial = minigame.utility(pirate.faction)
    hero.max_health -= 100
    assert utility_initial < minigame.utility(pirate.faction)


@pytest.mark.skip(reason="not supported")
def test_more_mana_is_better(minigame, hero):
    utility_initial = minigame.utility(hero.faction)
    hero.max_mana += 100
    assert utility_initial < minigame.utility(hero.faction)


@pytest.mark.skip(reason="not supported")
def test_more_stamina_is_better(minigame, hero):
    utility_initial = minigame.utility(hero.faction)
    hero.max_stamina += 100
    assert utility_initial < minigame.utility(hero.faction)


@pytest.mark.skip(reason="not supported")
def test_more_readiness_is_better(minigame, hero):
    utility_initial = minigame.utility(hero.faction)
    hero.readiness += 100
    assert utility_initial < minigame.utility(hero.faction)


def test_hurt_negative_delta(minigame, hero, no_chances, imba_ability):

    old_abilities = set(hero.actives)

    hero.give_active(imba_ability)
    hero.readiness += 10

    ability = list(set(hero.actives) - old_abilities)[0]
    choice = ability, hero
    delta = minigame.delta(choice)

    assert delta < 0


def test_small_hurt_negative_delta(
        minigame,
        hero,
        no_chances,
        tiny_imba_ability):

    old_abilities = set(hero.actives)

    hero.give_active(tiny_imba_ability)
    hero.readiness += 10

    ability = list(set(hero.actives) - old_abilities)[0]
    choice = ability, hero
    delta = minigame.delta(choice)

    assert delta < 0


def test_pirates_cry_too(minigame, pirate, no_chances, imba_ability):

    old_abilities = set(pirate.actives)

    pirate.give_active(imba_ability)
    pirate.readiness += 10

    ability = list(set(pirate.actives) - old_abilities)[0]

    choice = ability, pirate
    delta = minigame.delta(choice)

    assert delta < 0


def test_pirates_cry_too_a_little(
        minigame,
        pirate,
        no_chances,
        tiny_imba_ability):

    old_abilities = set(pirate.actives)

    pirate.give_active(tiny_imba_ability)
    pirate.readiness += 10

    ability = list(set(pirate.actives) - old_abilities)[0]

    delta = minigame.delta((ability, pirate))

    assert delta < 0


@pytest.mark.skip(reason="not supported")
def test_positions_can_go_out_of_utility(minigame):
    n_checked = 0

    for unit in minigame.units:
        choices = minigame.get_all_choices(unit)

        for c in choices:
            active, target = c
            if ActiveTags.MOVEMENT in active.tags:
                n_checked += 1

                delta = minigame.delta(c)
                assert delta == 0

    assert n_checked > 0
