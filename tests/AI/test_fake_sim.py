
def test_results_match(minigame, hero):

    count_simulated = 0

    choices = minigame.get_all_choices(hero)
    fraction = minigame.factions[hero]

    mismatches = []

    for c in choices:
        active, target = c
        if active.simulate_callback:
            count_simulated += 1
            fake_util = minigame.fake_measure(c, fraction)
            sim = minigame.step_into_sim(active, target)
            real_util = sim.utility(fraction)
            if fake_util != real_util:
                mismatches.append(c)

    assert len(mismatches) == 0
    assert count_simulated > 0


