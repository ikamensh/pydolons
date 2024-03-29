from __future__ import annotations


import copy
from functools import lru_cache
from typing import Set, TYPE_CHECKING, List
if TYPE_CHECKING:
    from DreamGame import DreamGame
    from mechanics.buffs import Ability
    from mechanics.actives import Cost
    from battlefield import Cell

from game_objects.battlefield_objects import BaseType, BattlefieldObject, CharAttributes as ca
from game_objects.battlefield_objects.CharAttributes import Constants
from game_objects.attributes import Attribute, AttributeWithBonuses, DynamicParameter
from game_objects import items
from mechanics.damage import Damage
from mechanics.damage import Resistances, Armor
from mechanics import events
from mechanics.actives import ActiveTags, Active
from mechanics.factions import Faction
from cntent.actives.std.std_movements import std_movements, turn_ccw, turn_cw
from cntent.actives.std.std_melee_attack import std_attacks
from character.masteries.Masteries import Masteries, MasteriesEnum
from battlefield import Facing

import random

class Unit(BattlefieldObject):


    str = AttributeWithBonuses("str_base", ca.STREINGTH)
    end = AttributeWithBonuses("end_base", ca.ENDURANCE)
    prc = AttributeWithBonuses("prc_base", ca.PERCEPTION)
    agi = AttributeWithBonuses("agi_base", ca.AGILITY)
    int = AttributeWithBonuses("int_base", ca.INTELLIGENCE)
    cha = AttributeWithBonuses("cha_base", ca.CHARISMA)

    max_health = AttributeWithBonuses("max_health_base", ca.HEALTH)
    max_mana = AttributeWithBonuses("max_mana_base", ca.MANA)
    max_stamina = AttributeWithBonuses("max_stamina_base", ca.STAMINA)
    _initiative = AttributeWithBonuses("initiative_base", ca.INITIATIVE)

    armor = AttributeWithBonuses("armor_base", ca.ARMOR)
    resists = AttributeWithBonuses("resists_base", ca.RESISTANCES)

    melee_precision = AttributeWithBonuses("melee_precision_base", ca.PRECISION)
    melee_evasion = AttributeWithBonuses("melee_evasion_base", ca.EVASION)


    health = DynamicParameter("max_health", [lambda u : events.UnitDiedEvent(u)])
    mana = DynamicParameter("max_mana")
    stamina = DynamicParameter("max_stamina")

    is_obstacle = False


    def __init__(self,
                 base_type: BaseType, *,
                 cell = None,
                 facing = Facing.NORTH,
                 faction = Faction.ENEMY,
                 game=None,
                 masteries: Masteries = None):
        super().__init__(cell)
        self.game: DreamGame = game
        self.readiness = 0
        self.disabled = False
        self.alive = True
        self.last_damaged_by = None
        self.fights_hero = None

        self.bonuses = frozenset()
        self.buffs = []
        self.abilities: List[Ability] = []

        self.inventory = items.Inventory(base_type.inventory_capacity, self)
        self.quick_items = items.QuickItems(base_type.quick_items, self)
        self.equipment = items.Equipment(self)
        self.xp = base_type.xp

        masteries = masteries or Masteries(base_type.xp)

        self.base_type = base_type
        self.masteries = masteries
        self.facing: complex = facing
        self.faction = faction

        self.update(base_type, masteries)


    def update(self, base_type = None, masteries = None):
        base_type = base_type or self.base_type
        self.str_base = Attribute.attribute_or_none(base_type.attributes[ca.STREINGTH])
        self.end_base = Attribute.attribute_or_none(base_type.attributes[ca.ENDURANCE])
        self.prc_base = Attribute.attribute_or_none(base_type.attributes[ca.PERCEPTION])
        self.agi_base = Attribute.attribute_or_none(base_type.attributes[ca.AGILITY])
        self.int_base = Attribute.attribute_or_none(base_type.attributes[ca.INTELLIGENCE])
        self.cha_base = Attribute.attribute_or_none(base_type.attributes[ca.CHARISMA])
        self.masteries = masteries or self.masteries


        self.type_name = base_type.type_name


        self.unarmed_damage_type = base_type.unarmed_damage_type
        self.unarmed_chances = base_type.unarmed_chances
        self.resists_base = Resistances(base_type.resists)
        self.natural_armor = Armor(base_type.armor_base, base_type.armor_dict)

        self.deactivate_abilities()

        self.abilities = []
        for abil in base_type.abilities:
            self.add_ability(abil())

        if isinstance(base_type.icon, str):
            self.icon = base_type.icon
        else:
            self.icon = random.choice(base_type.icon)

        self.sound_map = base_type.sound_map

        self.actives: List[Active] = []
        for active in base_type.actives:
            self.give_active(active)

        for slot in self.equipment:
            if slot.content:
                slot.content.on_equip(slot)

        for slot in self.quick_items:
            if slot.content:
                slot.content.on_equip(slot)



        self.turn_ccw_active = self.give_active(turn_ccw)
        self.turn_ccw = lambda: self.activate(self.turn_ccw_active)

        self.turn_cw_active = self.give_active(turn_cw)
        self.turn_cw = lambda: self.activate(self.turn_cw_active)

        for active in std_attacks:
            self.give_active(active)

        for active in std_movements:
            self.give_active(active)

    def deactivate_abilities(self):
        if self.abilities:
            for a in list(self.abilities):
                self.remove_ability(a)

    def add_ability(self, ability):
        if self.game:
            ability.apply_to(self)
        self.abilities.append(ability)
        self.recalc()

    def remove_ability(self, ability):
        ability.deactivate()
        self.abilities.remove(ability)
        self.recalc()

    def add_buff(self, buff):
        buff.apply_to(self)
        self.buffs.append(buff)
        self.recalc()

    def remove_buff(self, buff):
        buff.deactivate()
        self.buffs.remove(buff)
        self.recalc()

    def recalc(self):
        bonus_lists = [ability.bonus for ability in self.abilities if ability.bonus]
        bonus_lists += [buff.bonus for buff in self.buffs if buff.bonus]
        bonus_lists += self.equipment.bonuses
        self.bonuses = frozenset(bonus_lists)

    @property
    def sight_range(self):
        return 1 + (self.prc/4) ** (2/3)

    @property
    def armor_base(self):
        body_armor = self.equipment[items.EquipmentSlotUids.BODY]
        if body_armor:
            return body_armor.armor + self.natural_armor
        else:
            return self.natural_armor

    @property
    def max_health_base(self):
        return Attribute(self.end * Constants.HP_PER_END, 100, 0)

    @property
    def max_mana_base(self):
        return Attribute(self.int * Constants.MANA_PER_INT, 100, 0)

    @property
    def max_stamina_base(self):
        return Attribute(self.str * Constants.STAMINA_PER_STR, 100, 0)

    @property
    def initiative_base(self):
        return self.__initiative_formula(self.agi, self.int, self.stamina)

    @staticmethod
    @lru_cache()
    def __initiative_formula(agi, intel, stamina):
        return Attribute(1 + 9 * ((0.4 + agi / 25 + intel / 25) ** (3 / 5)) * ((stamina / (
                10*Constants.STAMINA_PER_STR)) ** (1 / 4)), 100, 0)

    @property
    def initiative(self):
        if self.disabled:
            return 0
        else:
            return self._initiative

    @property
    def melee_mastery(self):
        weapon = self.get_melee_weapon()
        return weapon.mastery or MasteriesEnum.UNARMED

    @property
    def melee_precision_base(self):
        mastery = self.masteries[self.melee_mastery]
        return Attribute(self.str + self.prc + mastery, 100, 0)


    @property
    def melee_evasion_base(self):
        return Attribute(self.prc*2 + self.agi*3, 100, 0)


    def reset(self):
        """Give unit maximum values for all dynamic attributes"""
        DynamicParameter.reset(self)

    @property
    def tooltip_info(self):
        return {'name':f"{self.type_name}_{self.uid}",
                'hp':str(int(self.health)),
                'mana':str(self.mana),
                'stamina':str(int(self.stamina)),

                'initiative': str(int(self.initiative)),

                'damage': str(int(self.get_melee_weapon().damage.amount)),
                'armor': repr(self.armor),

                'attack':str(self.melee_precision),
                'defence':str(self.melee_evasion),
                'cell:':str(self.cell)}


    def give_active(self, active) -> Active:
        cpy = copy.deepcopy(active)
        cpy.game = self.game
        self.actives.append(cpy)
        cpy.owner = self
        cpy.uid = int(cpy.uid * 1e7 + self.uid)
        return cpy

    def remove_active(self, active):
        searched_uid = int(active.uid * 1e7 + self.uid)
        active = [a for a in self.actives if a.uid == searched_uid][0]
        self.actives.remove(active)


    def activate(self, active: Active, user_targeting = None):
        active.owner = self
        return active.activate(user_targeting)

    @property
    def movement_actives(self):
        return [active for active in self.actives if ActiveTags.MOVEMENT in active.tags]

    @property
    def attack_actives(self):
        return [active for active in self.actives if ActiveTags.ATTACK in active.tags]


    def get_unarmed_weapon(self):
        dmg = Damage(amount=self.str * Constants.UNARMED_DAMAGE_PER_STR, type=self.unarmed_damage_type)
        return items.Weapon(name="Fists", damage=dmg, chances=self.unarmed_chances, is_ranged=False,
                      mastery=MasteriesEnum.UNARMED, game=self.game)


    def get_melee_weapon(self):
        weapon = self.equipment[items.EquipmentSlotUids.HANDS]
        if weapon and not weapon.is_ranged:
            return weapon
        else:
            return self.get_unarmed_weapon()

    def get_ranged_weapon(self):
        weapon = self.equipment[items.EquipmentSlotUids.HANDS]
        if weapon and weapon.is_ranged:
            return weapon

    def can_pay(self, cost: Cost):
        return not any( [
            cost.mana > self.mana,
            cost.stamina > self.stamina,
            cost.health > self.health])



    def pay(self, cost):
        self.mana -= cost.mana
        self.stamina -= cost.stamina
        self.lose_health(cost.health, self)
        self.readiness -= cost.readiness

    def lose_health(self, dmg_amount, source=None):
        assert dmg_amount >= 0
        if source:
            self.last_damaged_by = source

        self.health -= dmg_amount

    @property
    def attacks(self):
        return [a for a in self.actives if ActiveTags.ATTACK in a.tags]



    def __repr__(self):
        return f"{self.type_name} {self.uid} with {self.health :.0f} HP"
