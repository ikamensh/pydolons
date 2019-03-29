
def test_concept_to_spell(lightning_concept, double_damage_rune):
    spell1 = lightning_concept.to_spell([])
    spell2 = lightning_concept.to_spell([double_damage_rune])

    assert spell2.amount > spell1.amount
    assert spell2.complexity > spell1.complexity
