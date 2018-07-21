class AttributeWithBonuses:

    def __init__(self, name_base, bonus_enum):
        cls = self.__class__
        prefix = cls.__name__
        self.base_name = name_base
        self.attrib_enum = bonus_enum
        self.storage_name = f"{prefix}_{name_base}".replace("base","")

    def __get__(self, instance, owner):
        return self.sum_with_bonuses(instance)

    def sum_with_bonuses(self, instance):
        attr = getattr(instance, self.base_name)
        for bonus in instance.bonuses:
            matching_bonus = bonus[self.attrib_enum]
            if matching_bonus:
                attr += matching_bonus
        return attr.value()




