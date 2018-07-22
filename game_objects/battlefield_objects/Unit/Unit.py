from game_objects.battlefield_objects.Unit.BaseType import BaseType
from game_objects.battlefield_objects.attributes import Attribute, AttributeWithBonuses, DynamicParameter
from game_objects.battlefield_objects.attributes import AttributesEnum
from game_objects.items import Inventory, Equipment, Weapon
from mechanics.damage import Damage
from mechanics.damage import Resistances, Armor
from mechanics.events import UnitDiedEvent
from my_utils.utils import flatten


class Unit:
    HP_PER_STR = 25
    STAMINA_PER_END = 10
    MANA_PER_INT = 15
    UNARMED_DAMAGE_PER_STR = 5

    str = AttributeWithBonuses("str_base", AttributesEnum.STREINGTH)
    end = AttributeWithBonuses("end_base", AttributesEnum.ENDURANCE)
    prc = AttributeWithBonuses("prc_base", AttributesEnum.PERCEPTION)
    agi = AttributeWithBonuses("agi_base", AttributesEnum.AGILITY)
    int = AttributeWithBonuses("int_base", AttributesEnum.INTELLIGENCE)
    cha = AttributeWithBonuses("cha_base", AttributesEnum.CHARISMA)

    max_health = AttributeWithBonuses("max_health_base", AttributesEnum.HEALTH)
    max_mana = AttributeWithBonuses("max_mana_base", AttributesEnum.MANA)
    max_stamina = AttributeWithBonuses("max_stamina_base", AttributesEnum.STAMINA)
    _initiative = AttributeWithBonuses("initiative_base", AttributesEnum.INITIATIVE)


    health = DynamicParameter("max_health")
    mana = DynamicParameter("max_mana")
    stamina = DynamicParameter("max_stamina")

    
    def __init__(self, base_type: BaseType):
        self.str_base = Attribute(base_type.attributes[AttributesEnum.STREINGTH], 100, 0)
        self.end_base = Attribute(base_type.attributes[AttributesEnum.ENDURANCE], 100, 0)
        self.prc_base = Attribute(base_type.attributes[AttributesEnum.PERCEPTION], 100, 0)
        self.agi_base = Attribute(base_type.attributes[AttributesEnum.AGILITY], 100, 0)
        self.int_base = Attribute(base_type.attributes[AttributesEnum.INTELLIGENCE], 100, 0)
        self.cha_base = Attribute(base_type.attributes[AttributesEnum.CHARISMA], 100, 0)
        self.readiness = 0
        self.disabled = False

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
        return self.str + self.agi

    @property
    def melee_evasion(self):
        return self.prc + self.agi



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
        return Weapon(name="Fists", damage=dmg)


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

        return result

    def pay(self, cost):
        self.mana -= cost.mana
        self.stamina -= cost.stamina

    #todo replace with getter and setter... interesting.
    def lose_health(self, dmg_amount, source):
        """
        :param dmg_amount: amount of incoming damage
        :return: True if unit lost all HP, False otherwise
        """
        assert dmg_amount >= 0
        self.health -= dmg_amount
        if self.health <= 0:
            UnitDiedEvent(self, source)
            return True
        else:
            return False


    def __repr__(self):
        return f"{self.type_name} with {self.health} HP"