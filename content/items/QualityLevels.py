from collections import namedtuple
QualityLevel = namedtuple("quality_level", "name rarity")

class QualityLevels:
    CRUDE = QualityLevel("Crude", 0.6)
    PRIMITIVE = QualityLevel("Primitive", 0.8)
    USUAL = QualityLevel("Usual", 1)
    SUPERIOR = QualityLevel("Superior", 1.15)
    MASTERPIECE = QualityLevel("Masterpiece", 1.3)
    LEGENDARY = QualityLevel("Legendary", 1.45)