from game_objects.battlefield_objects import BaseType, BattlefieldObject, CharAttributes as ca
from game_objects.battlefield_objects.CharAttributes import HP_PER_STR, MANA_PER_INT, STAMINA_PER_END, UNARMED_DAMAGE_PER_STR
from game_objects.attributes import Attribute, AttributeWithBonuses, DynamicParameter
from game_objects.items import Inventory, Equipment, Weapon
from mechanics.damage import Damage
from mechanics.damage import Resistances, Armor
from mechanics import events
from mechanics.actives import ActiveTags
from content.actives.std_movements import std_movements, turn_ccw, turn_cw
from content.actives.std_melee_attack import std_attacks
from my_utils.utils import flatten
from character_creation.Masteries import Masteries, MasteriesEnum

import copy
from functools import lru_cache

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



    health = DynamicParameter("max_health", [events.UnitDiedEvent])
    mana = DynamicParameter("max_mana")
    stamina = DynamicParameter("max_stamina")



    last_uid = 0

    def __init__(self, base_type: BaseType, masteries = None):
        Unit.last_uid += 1
        self.uid = Unit.last_uid

        self.str_base = Attribute.attribute_or_none(base_type.attributes[ca.STREINGTH])
        self.end_base = Attribute.attribute_or_none(base_type.attributes[ca.ENDURANCE])
        self.prc_base = Attribute.attribute_or_none(base_type.attributes[ca.PERCEPTION])
        self.agi_base = Attribute.attribute_or_none(base_type.attributes[ca.AGILITY])
        self.int_base = Attribute.attribute_or_none(base_type.attributes[ca.INTELLIGENCE])
        self.cha_base = Attribute.attribute_or_none(base_type.attributes[ca.CHARISMA])
        self.readiness = 0
        self.disabled = False
        self.masteries = masteries or Masteries(base_type.xp)
        self.xp = base_type.xp

        self.type_name = base_type.type_name
        self.actives = set(base_type.actives)

        self.unarmed_damage_type = base_type.unarmed_damage_type
        self.unarmed_chances = base_type.unarmed_chances
        self.resists_base = Resistances(base_type.resists)
        self.natural_armor = Armor(base_type.armor_base, base_type.armor_dict)

        self.inventory = Inventory(base_type.inventory_capacity, self)
        self.equipment :Equipment = Equipment(self)
        self._abilities = []
        self._buffs = []
        self.bonuses = frozenset()

        self.alive = True
        self.is_obstacle = False
        self.last_damaged_by = None

        self.icon = base_type.icon
        self.sound_map = base_type.sound_map

        self.turn_ccw_active = self.give_active(turn_ccw)
        self.turn_ccw = lambda : self.activate(self.turn_ccw_active)

        self.turn_cw_active = self.give_active(turn_cw)
        self.turn_cw = lambda : self.activate(self.turn_cw_active)

        for active in std_attacks:
            self.give_active(active)

        for active in std_movements:
            self.give_active(active)


    def add_ability(self, ability):
        self._abilities.append(ability)
        self.recalc()

    def remove_ability(self, ability):
        self._abilities.remove(ability)
        self.recalc()

    def add_buff(self, buff):
        self._buffs.append(buff)
        self.recalc()

    def remove_buff(self, buff):
        self._buffs.remove(buff)
        self.recalc()

    def recalc(self):
        bonus_lists = [ability.bonuses for ability in self._abilities if ability.bonuses]
        bonus_lists += [buff.bonuses for buff in self._buffs if buff.bonuses]
        bonus_lists += self.equipment.bonuses
        self.bonuses = frozenset(flatten(bonus_lists))

    @property
    def sight_range(self):
        return 1 + (self.prc/4) ** (2/3)

    @property
    def armor_base(self):
        body_armor = self.equipment["body"]
        if body_armor:
            return body_armor.armor + self.natural_armor
        else:
            return self.natural_armor

    @property
    def max_health_base(self):
        return Attribute(self.str * HP_PER_STR, 100, 0)

    @property
    def max_mana_base(self):
        return Attribute(self.int * MANA_PER_INT, 100, 0)

    @property
    def max_stamina_base(self):
        return Attribute(self.end * STAMINA_PER_END, 100, 0)

    @property
    def initiative_base(self):
        return self.__initiative_formula(self.agi, self.stamina)

    @lru_cache(maxsize=16)
    def __initiative_formula(self, agi, stamina):
        return Attribute(10 * ((0.4 + agi / 14) ** (3 / 5)) * ((stamina / 100) ** (1 / 3)), 100, 0)

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
    def melee_precision(self):
        mastery = self.masteries[self.melee_mastery]
        return self.str + self.agi + mastery

    @property
    def melee_evasion(self):
        return self.prc*2 + self.agi*3

    def reset(self):
        """
        Give unit maximum values for all dynamic attributes
        """
        DynamicParameter.reset(self)


    def give_active(self, active):
        cpy = copy.deepcopy(active)
        self.actives.add(cpy)
        cpy.owner = self
        cpy.uid = int(cpy.uid * 1e7 + self.uid)
        return cpy

    #TODO create target method that prompts the game to get right kind of targeting from the user
    def activate(self, active, user_targeting = None):
        assert active in self.actives
        assert active.owner is self
        active.activate(user_targeting)

    @property
    def movement_actives(self):
        return [active for active in self.actives if ActiveTags.MOVEMENT in active.tags]

    @property
    def attack_actives(self):
        return [active for active in self.actives if ActiveTags.ATTACK in active.tags]


    def get_unarmed_weapon(self):
        dmg = Damage(amount=self.str * UNARMED_DAMAGE_PER_STR, type=self.unarmed_damage_type)
        return Weapon(name="Fists", damage=dmg, mastery=MasteriesEnum.UNARMED)


    def get_melee_weapon(self):
        weapon = self.equipment["hands"]
        if weapon:
            return weapon
        else:
            return self.get_unarmed_weapon()

    def can_pay(self, cost):
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


    def __repr__(self):
        return f"{self.type_name} {self.uid} with {self.health} HP"
