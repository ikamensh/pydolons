class AttributeWithBonuses:

    def __init__(self, name_base, bonus_enum):
        cls = self.__class__
        prefix = cls.__name__
        self.base_name = name_base
        self.attrib_enum = bonus_enum
        self.storage_name = f"{prefix}_{name_base}".replace("base","")

    def __get__(self, instance, owner):
        return self.sum_with_abilities(instance)

    def sum_with_abilities(self, instance):
        attr = getattr(instance, self.base_name)
        for ability in instance.abilities:
            bonus = ability[self.attrib_enum]
            if bonus:
                attr += bonus
        return attr.value()




