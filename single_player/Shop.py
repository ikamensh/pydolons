from __future__ import annotations
import random
from game_objects.items.materials.MaterialTypes import MaterialTypes
from typing import TYPE_CHECKING, List, Dict
if TYPE_CHECKING:
    from game_objects.items import Blueprint, Material, QualityLevel


def generate_assortment(blueprints: List[Blueprint], materials: Dict[MaterialTypes:List[Material]], quality_levels: List[QualityLevel]):

    for bp in blueprints:
        assert bp.material_type in materials

    assortment = []

    for i in range(100):
        bp = random.choice(blueprints)
        matching_materials = materials[bp.material_type]
        material = random.choice(matching_materials)
        quality = random.choice(quality_levels)

        assortment.append(bp.to_item(material, quality))

    return sorted(assortment, key=lambda x:x.price)


from cntent.items.materials.materials import Stones, Metals, Leathers, Woods
from cntent.items.blueprints.weapons.weapons import fancy_blueprints, std_blueprints
from cntent.items.blueprints.armor.body_armor import leather_outfit, pirate_jacket, cuirass, scalemail
from cntent.items.QualityLevels import QualityLevels

all_armor = [leather_outfit, pirate_jacket, cuirass, scalemail]
all_blueprints = all_armor + std_blueprints + fancy_blueprints
mt = MaterialTypes
all_materials = {mt.STONE: Stones.all, mt.METAL: Metals.all, mt.WOOD: Woods.all, mt.SKIN: Leathers.all}


# itemz = generate_assortment(all_blueprints, all_materials, QualityLevels.all)
#
# for item in itemz:
#     print(item, item.price)


from game_objects.items import Inventory

def total_value(items, mod):
    return sum([mod(i.value) for i in items])


from my_utils.utils import tractable_value

def price_buy(orig_price, trust,  baseline):
    expensive_factor = orig_price / baseline

    if expensive_factor < 1:
        factor = expensive_factor ** (4/3)
    else:
        factor = expensive_factor ** (3/4)

    return tractable_value ( trust * orig_price * factor / expensive_factor  , digits=3)
    # return tractable_value ( trust * orig_price  , digits=3)


def price_sell(orig_price, trust, baseline):
    expensive_factor = orig_price / baseline

    if expensive_factor < 1:
        factor = expensive_factor ** (3 / 4)
    else:
        factor = expensive_factor ** (4 / 3)

    # print(expensive_factor, factor)
    return tractable_value( 1 / trust * orig_price * factor / expensive_factor , digits=3)
    # return tractable_value( 1 / trust * orig_price  , digits=3)


class Shop:

    def __init__(self, assortment, trust, baseline):

        self.inventory = Inventory(len(assortment) * 2 + 50, self)
        for item in assortment:
            self.inventory.add(item)

        self.trust = trust
        self.baseline = baseline

    def _price_sell(self, price):
        return price_sell(price, self.trust, self.baseline)

    def _price_buy(self, price):
        return price_buy(price, self.trust, self.baseline)

    def display_inventory(self):
        for item in self.inventory.all_items():
            print(item, item.price, self._price_buy(item.price), self._price_sell(item.price))




shop = Shop(generate_assortment(all_blueprints, all_materials, QualityLevels.all), 1, 500)
shop.display_inventory()