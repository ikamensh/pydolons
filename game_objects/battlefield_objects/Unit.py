from game_objects.battlefield_objects.BaseType import BaseType
from game_objects.attributes import Attribute, AttributeWithBonuses, DynamicParameter
from game_objects.battlefield_objects import CharAttributes
from game_objects.items import Inventory, Equipment, Weapon
from mechanics.damage import Damage
from mechanics.damage import Resistances, Armor
from mechanics.events import UnitDiedEvent
from my_utils.utils import flatten

from character_creation.Masteries import Masteries, MasteriesEnum


class Unit:
    HP_PER_STR = 25
    STAMINA_PER_END = 10
    MANA_PER_INT = 10
    UNARMED_DAMAGE_PER_STR = 5

    str = AttributeWithBonuses("str_base", CharAttributes.STREINGTH)
    end = AttributeWithBonuses("end_base", CharAttributes.ENDURANCE)
    prc = AttributeWithBonuses("prc_base", CharAttributes.PERCEPTION)
    agi = AttributeWithBonuses("agi_base", CharAttributes.AGILITY)
    int = AttributeWithBonuses("int_base", CharAttributes.INTELLIGENCE)
    cha = AttributeWithBonuses("cha_base", CharAttributes.CHARISMA)

    max_health = AttributeWithBonuses("max_health_base", CharAttributes.HEALTH)
    max_mana = AttributeWithBonuses("max_mana_base", CharAttributes.MANA)
    max_stamina = AttributeWithBonuses("max_stamina_base", CharAttributes.STAMINA)
    _initiative = AttributeWithBonuses("initiative_base", CharAttributes.INITIATIVE)


    health = DynamicParameter("max_health", [UnitDiedEvent])
    mana = DynamicParameter("max_mana")
    stamina = DynamicParameter("max_stamina")

    
    def __init__(self, base_type: BaseType, masteries = None):
        self.str_base = Attribute.attribute_or_none(base_type.attributes[CharAttributes.STREINGTH])
        self.end_base = Attribute.attribute_or_none(base_type.attributes[CharAttributes.ENDURANCE])
        self.prc_base = Attribute.attribute_or_none(base_type.attributes[CharAttributes.PERCEPTION])
        self.agi_base = Attribute.attribute_or_none(base_type.attributes[CharAttributes.AGILITY])
        self.int_base = Attribute.attribute_or_none(base_type.attributes[CharAttributes.INTELLIGENCE])
        self.cha_base = Attribute.attribute_or_none(base_type.attributes[CharAttributes.CHARISMA])
        self.readiness = 0
        self.disabled = False
        self.masteries = masteries or Masteries(base_type.xp)

        self.type_name = base_type.type_name
        self.actives = base_type.actives

        self.unarmed_damage_type = base_type.unarmed_damage_type
        self.unarmed_chances = base_type.unarmed_chances
        self.resists = Resistances(base_type.resists)
        self.natural_armor = Armor(base_type.armor_base, base_type.armor_dict)

        self.inventory = Inventory(base_type.inventory_capacity, self)
        self.equipment :Equipment = base_type.equipment_cls(self)
        self.abilities = []
        self.buffs = []

        self.alive = True
        self.last_damaged_by = None

        self.icon = base_type.icon


    @property
    def bonuses(self):
        bonus_lists = [ability.bonuses for ability in self.abilities if ability.bonuses]
        bonus_lists += [buff.bonuses for buff in self.buffs if buff.bonuses]
        bonuses = list( flatten(bonus_lists))

        return bonuses

    @property
    def armor(self):
        body_armor = self.equipment["body"]
        if body_armor:
            return body_armor.armor + self.natural_armor
        else:
            return self.natural_armor

    @property
    def max_health_base(self):
        return Attribute(self.str * Unit.HP_PER_STR, 100, 0)

    @property
    def max_mana_base(self):
        return Attribute(self.int * Unit.MANA_PER_INT, 100, 0)

    @property
    def max_stamina_base(self):
        return Attribute(self.end * Unit.STAMINA_PER_END, 100, 0)

    @property
    def initiative_base(self):
        return Attribute(10 * ((0.4 + self.agi / 14) ** (3 / 5)) * ((self.stamina / 100) ** (1 / 3)), 100, 0)

    @property
    def initiative(self):
        if self.disabled:
            return 0
        else:
            return self._initiative


    @property
    def melee_precision(self):
        weapon = self.get_melee_weapon()
        mastery = self.masteries[weapon.mastery or MasteriesEnum.UNARMED]
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
        self.actives.add(active)
        active.assign_to_unit(self)

    #TODO create target method that prompts the game to get right kind of targeting from the user
    def activate(self, active, user_targeting):
        assert active in self.actives
        active.activate(user_targeting)


    def get_unarmed_weapon(self):
        dmg = Damage(amount=self.str * Unit.UNARMED_DAMAGE_PER_STR, type=self.unarmed_damage_type)
        return Weapon(name="Fists", damage=dmg, mastery=MasteriesEnum.UNARMED)


    def get_melee_weapon(self):
        weapon = self.equipment["hands"]
        if weapon:
            return weapon
        else:
            return self.get_unarmed_weapon()

    def can_pay(self, cost):
        result = True
        if cost.mana > self.mana:
            result = False
        if cost.stamina > self.stamina:
            result = False
        if cost.health > self.health:
            result = False

        return result

    def pay(self, cost):
        self.mana -= cost.mana
        self.stamina -= cost.stamina
        self.lose_health(cost.health, self)
        self.readiness -= cost.readiness

    def lose_health(self, dmg_amount, source):
        assert dmg_amount >= 0
        self.last_damaged_by = source
        self.health -= dmg_amount



    def __repr__(self):
        return f"{self.type_name} with {self.health} HP"