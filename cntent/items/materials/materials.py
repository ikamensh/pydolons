from game_objects.items.materials.Materials import Material
from game_objects.items import MaterialTypes as mt


class Metals:
    bronze = Material(mt.METAL, "bronze", 1.1)
    iron = Material(mt.METAL, "iron", 1.4)
    steel = Material(mt.METAL, "steel", 1.8)
    mithril = Material(mt.METAL, "mithril", 2.4, energy=75)
    adamant = Material(mt.METAL, "adamant", 2.6, magic_complexity=1.15)

    all = [bronze, iron, steel, mithril]


class Stones:
    stone = Material(mt.STONE, "stone", 0.7)
    granite = Material(mt.STONE, "granite", 0.85)
    flintstone = Material(mt.STONE, "flintstone", 1.15)
    blackrock = Material(mt.STONE, "blackrock", 1.45)
    obsidian = Material(
        mt.STONE,
        "obsidian",
        1.7,
        magic_complexity=1.2,
        energy=125)
    corundum = Material(mt.STONE, "corundum", 3.3)

    all = [stone, granite, flintstone, blackrock, obsidian, corundum]


class Leathers:
    skin = Material(mt.SKIN, "skin", 0.65)
    thick_skin = Material(mt.SKIN, "thick_skin", 0.85)
    lizard_skin = Material(mt.SKIN, "lizard_skin", 1)
    green_troll_skin = Material(mt.SKIN, "green troll skin", 1.6, energy=100)
    black_troll_skin = Material(mt.SKIN, "black troll skin", 2, energy=125)
    green_dragon_skin = Material(
        mt.SKIN,
        "green dragon skin",
        2.5,
        magic_complexity=1.4)
    red_dragon_skin = Material(
        mt.SKIN,
        "red dragon skin",
        2.7,
        magic_complexity=1.5)
    black_dragon_skin = Material(
        mt.SKIN,
        "black dragon skin",
        3,
        magic_complexity=1.6)

    all = [
        skin,
        thick_skin,
        lizard_skin,
        green_troll_skin,
        black_troll_skin,
        green_dragon_skin,
        black_dragon_skin,
        red_dragon_skin]


class Woods:
    wood = Material(mt.WOOD, "wood", 0.7)
    oak = Material(mt.WOOD, "oak", 1, energy=75)
    black_wood = Material(mt.WOOD, "black wood", 1.2)
    firewood = Material(mt.WOOD, "firewood", 1.45, magic_complexity=1.2)
    cadamba_tree = Material(mt.WOOD, "cadamba", 1.7, magic_complexity=1.3)
    world_tree = Material(mt.WOOD, "world tree", 2.3, energy=150)

    all = [wood, oak, black_wood, firewood, cadamba_tree, world_tree]


if __name__ == "__main__":
    for mt in [Woods, Leathers, Metals, Stones]:
        print("  ")
        print(mt)
        for m in mt.all:
            print(m, m.price)
