class ChanceCalculator:
    advantage_to_double = 25

    @staticmethod
    def chance(base_prob, precision, evasion):
        assert 0 <= base_prob <= 1
        if base_prob == 0 or base_prob == 1:
            return base_prob

        if precision == evasion:
            return base_prob

        if evasion > precision:
            adv = 1 + (evasion - precision) / ChanceCalculator.advantage_to_double
        else:
            adv = 1 / (1 + (precision - evasion) / ChanceCalculator.advantage_to_double)


        new_chance = base_prob ** adv    # Note: as base_prob is below one, powers below one increase the chance, and powers over one drop it.
        # print("BASE PROB:", base_prob, "ADV", adv, "NEW CHANCE", new_chance)

        assert 0 <= new_chance <= 1
        return new_chance



if __name__ == "__main__":

    for base_chance in [0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]:
        for attack in [0, 10, 33, 100, 333]:
            for defense in [0, 10, 33, 100, 333]:
                print(base_chance, attack, defense, ChanceCalculator.chance(base_chance, attack, defense))