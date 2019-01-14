from pytest import fixture

from single_player.Shop import Shop, generate_assortment


@fixture()
def assortment():
    from cntent.items.materials.materials import Stones, Metals, Leathers, Woods
    from cntent.items.blueprints.weapons.weapons import fancy_blueprints, std_blueprints
    from cntent.items.blueprints.armor.body_armor import leather_outfit, pirate_jacket, cuirass, scalemail
    from cntent.items.QualityLevels import QualityLevels

    all_armor = [leather_outfit, pirate_jacket, cuirass, scalemail]
    all_blueprints = all_armor + std_blueprints + fancy_blueprints
    from game_objects.items.materials.MaterialTypes import MaterialTypes
    mt = MaterialTypes
    all_materials = {mt.STONE: Stones.all, mt.METAL: Metals.all, mt.WOOD: Woods.all, mt.SKIN: Leathers.all}

    return generate_assortment(all_blueprints, all_materials, QualityLevels.all)

@fixture()
def shop(assortment):
    return Shop(assortment, 1, 500)

@fixture()
def customer():
    from character.Character import Character
    from cntent.base_types import demohero_basetype

    char = Character(demohero_basetype)
    char.gold = 1e6
    return char


def test_transactions(shop, customer):

    shop.customer = customer
    items_in_shop = lambda : len(shop.inventory.all_items)
    items_hero_has = lambda : len(customer.unit.inventory.all_items)

    assert items_in_shop() > 10
    assert items_hero_has() == 0

    starting_money = customer.gold
    starting_assortment = items_in_shop()
    starting_belongings = items_hero_has()

    shop.buy( shop.inventory[3] )

    assert customer.gold < starting_money
    assert starting_assortment > items_in_shop()
    assert starting_belongings < items_hero_has()

    money_after_buying = customer.gold

    shop.sell(customer.unit.inventory[0])

    assert starting_money > customer.gold > money_after_buying
    assert starting_assortment == items_in_shop()
    assert starting_belongings == items_hero_has()



