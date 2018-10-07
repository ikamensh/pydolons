from game_objects.items.materials.Materials import Material
from game_objects.items import MaterialTypes


class Metals:
    bronze = Material(MaterialTypes.METAL, "bronze", 1.3)
    iron = Material(MaterialTypes.METAL, "iron", 1.6)
    steel = Material(MaterialTypes.METAL, "steel", 2.1)
    mithril = Material(MaterialTypes.METAL, "mithril", 2.5)


class Stones:
    stone = Material(MaterialTypes.STONE, "stone", 0.5)
    granite = Material(MaterialTypes.STONE, "granite", 0.75)
    flintstone = Material(MaterialTypes.STONE, "flintstone", 1.15)
    obsidian = Material(MaterialTypes.STONE, "obsidian", 1.4)


class Leathers:
    thin_skin = Material(MaterialTypes.SKIN, "thin skin", 0.5)
    skin = Material(MaterialTypes.SKIN, "skin", 0.65)
    thick_skin = Material(MaterialTypes.SKIN, "thick_skin", 0.85)
    lizard_skin = Material(MaterialTypes.SKIN, "lizard_skin", 1)
    troll_skin = Material(MaterialTypes.SKIN, "troll_skin", 2, energy=150)
    dragon_skin = Material(MaterialTypes.SKIN, "dragon_skin", 4, magic_complexity=2)