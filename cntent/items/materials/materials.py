from game_objects.items.materials.Materials import Material
from game_objects.items import MaterialTypes as mt


class Metals:
    bronze = Material(mt.METAL, "bronze", 1.3)
    iron = Material(mt.METAL, "iron", 1.6)
    steel = Material(mt.METAL, "steel", 2.1)
    mithril = Material(mt.METAL, "mithril", 2.5)


class Stones:
    stone = Material(mt.STONE, "stone", 0.5)
    granite = Material(mt.STONE, "granite", 0.75)
    flintstone = Material(mt.STONE, "flintstone", 1.15)
    obsidian = Material(mt.STONE, "obsidian", 1.4)


class Leathers:
    thin_skin = Material(mt.SKIN, "thin skin", 0.5)
    skin = Material(mt.SKIN, "skin", 0.65)
    thick_skin = Material(mt.SKIN, "thick_skin", 0.85)
    lizard_skin = Material(mt.SKIN, "lizard_skin", 1)
    troll_skin = Material(mt.SKIN, "troll_skin", 2, energy=150)
    dragon_skin = Material(mt.SKIN, "dragon_skin", 4, magic_complexity=2)


class Woods:
    wood = Material(mt.WOOD, "wood", 0.6)
    oak = Material(mt.WOOD, "oak", 0.9, energy=75)
    black_wood = Material(mt.WOOD, "black wood", 1.1)
    cadamba_tree = Material(mt.WOOD, "cadamba", 1.25, magic_complexity=1.4)
    world_tree = Material(mt.WOOD, "world tree", 2.1, energy=150)