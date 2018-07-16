from collections import namedtuple
QualityLevel = namedtuple("quality_level", "name rarity")

class QualityLevels:
    CRUDE = QualityLevel("Crude", 0.6)
    PRIMITIVE = QualityLevel("Crude", 0.8)
    USUAL = QualityLevel("Crude", 1)
    SUPERIOR = QualityLevel("Crude", 1.15)
    MASTERPIECE = QualityLevel("Crude", 1.35)
    LEGENDARY = QualityLevel("Crude", 1.55)