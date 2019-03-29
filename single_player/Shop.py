from __future__ import annotations
from my_utils.utils import tractable_value, kmb_number_display as kmb
from game_objects.items import Inventory
from cntent.items.QualityLevels import QualityLevels
from cntent.items.blueprints.armor.body_armor import leather_outfit, pirate_jacket, cuirass, scalemail
from cntent.items.blueprints.weapons.weapons import fancy_blueprints, std_blueprints
from cntent.items.materials.materials import Stones, Metals, Leathers, Woods
import random
from game_objects.items.materials.MaterialTypes import MaterialTypes
from typing import TYPE_CHECKING, List, Dict
if TYPE_CHECKING:
    from game_objects.items import Blueprint, Material, QualityLevel
    from game_objects.items import Slot


def generate_assortment(blueprints: List[Blueprint],
                        materials: Dict[MaterialTypes:List[Material]],
                        quality_levels: List[QualityLevel],
                        n=100):

    for bp in blueprints:
        assert bp.material_type in materials

    assortment = []

    for i in range(n):
        bp = random.choice(blueprints)
        matching_materials = materials[bp.material_type]
        material = random.choice(matching_materials)
        quality = random.choice(quality_levels)

        assortment.append(bp.to_item(material, quality))

    return sorted(assortment, key=lambda x: x.price)


all_armor = [leather_outfit, pirate_jacket, cuirass, scalemail]
all_blueprints = all_armor + std_blueprints + fancy_blueprints
mt = MaterialTypes
all_materials = {
    mt.STONE: Stones.all,
    mt.METAL: Metals.all,
    mt.WOOD: Woods.all,
    mt.SKIN: Leathers.all}


# itemz = generate_assortment(all_blueprints, all_materials, QualityLevels.all)
#
# for item in itemz:
#     print(item, item.price)


# def total_value(items, mod):
#     return sum([mod(i.value) for i in items])


def price_buy(orig_price, trust, baseline):
    expensive_factor = orig_price / baseline

    if expensive_factor < 1:
        factor = expensive_factor ** (4 / 3)
    else:
        factor = expensive_factor ** (3 / 4)

    return tractable_value(
        trust *
        orig_price *
        factor /
        expensive_factor,
        digits=3)
    # return tractable_value ( trust * orig_price  , digits=3)


def price_sell(orig_price, trust, baseline):
    expensive_factor = orig_price / baseline

    if expensive_factor < 1:
        factor = expensive_factor ** (3 / 4)
    else:
        factor = expensive_factor ** (4 / 3)

    # print(expensive_factor, factor)
    return tractable_value(
        1 /
        trust *
        orig_price *
        factor /
        expensive_factor,
        digits=3)
    # return tractable_value( 1 / trust * orig_price  , digits=3)


class Shop:

    def __init__(
            self,
            assortment,
            trust=1,
            baseline=500,
            customer: Character = None):

        self.inventory = Inventory(len(assortment) * 2 + 50, None)
        for item in assortment:
            self.inventory.add(item)

        self.trust = trust
        self.baseline = baseline
        self.customer = customer

    def price_high(self, price):
        return price_sell(price, self.trust, self.baseline)

    def price_low(self, price):
        return price_buy(price, self.trust, self.baseline)

    def display_inventory(self):
        for item in self.inventory.all_items:
            print(
                item, kmb(
                    item.price), kmb(
                    self.price_low(
                        item.price)), kmb(
                    self.price_high(
                        item.price)))

    def buy(self, inventory_slot: Slot):
        assert inventory_slot in self.inventory

        item = inventory_slot.content
        assert item is not None

        price = self.price_high(item.price)

        if self.customer.gold >= price and self.customer.unit.inventory.empty_slots:
            self.customer.gold -= price
            item = inventory_slot.pop_item()
            self.customer.unit.inventory.add(item)

    def sell(self, inventory_slot: Slot):
        assert inventory_slot in self.customer.unit.inventory

        item = inventory_slot.content
        assert item is not None

        price = self.price_low(item.price)

        self.customer.gold += price
        item = inventory_slot.pop_item()
        self.inventory.add(item)


if __name__ == "__main__":

    from character.Character import Character
    from cntent.base_types import demohero_basetype

    char = Character(demohero_basetype)
    char.gold = 1e6

    shop = Shop(
        generate_assortment(
            all_blueprints,
            all_materials,
            QualityLevels.all),
        1,
        500,
        customer=char)
    shop.display_inventory()

    print("testing")
