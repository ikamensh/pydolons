from game_objects.items.materials.Materials import MaterialTypes, Material

class Metals:
    bronze = Material(MaterialTypes.METAL, "bronze", 0.5)
    iron = Material(MaterialTypes.METAL, "iron", 0.75)
    steel = Material(MaterialTypes.METAL, "steel", 1)
    mithril = Material(MaterialTypes.METAL, "mithril", 1.15)