from game_objects.items import QualityLevel


class QualityLevels:
    CRUDE = QualityLevel("Crude", 0.6)
    PRIMITIVE = QualityLevel("Primitive", 0.8)
    USUAL = QualityLevel("Usual", 1)
    SUPERIOR = QualityLevel("Superior", 1.15)
    MASTERPIECE = QualityLevel("Masterpiece", 1.3)
    LEGENDARY = QualityLevel("Legendary", 1.45)

    all = [CRUDE, PRIMITIVE, USUAL, SUPERIOR, MASTERPIECE, LEGENDARY]
