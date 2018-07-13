from mechanics.PrecisionEvasion.ChanceCalculator import ChanceCalculator

for base_chance in [0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]:
    for attack in [0, 10, 33, 100, 333]:
        for defense in [0, 10, 33, 100, 333]:
            print(base_chance, attack, defense, ChanceCalculator.chance(base_chance, attack, defense))