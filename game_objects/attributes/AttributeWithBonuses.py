from functools import lru_cache


class AttributeWithBonuses:

    def __init__(self, name_base, bonus_enum):
        self.base_name = name_base
        self.attrib_enum = bonus_enum

    def __get__(self, instance, owner):
        attr = getattr(instance, self.base_name)
        return self.sum_with_bonuses(attr, instance.bonuses)

    @lru_cache()
    def sum_with_bonuses(self, attr, bonuses):
        if attr is None:
            return None
        for bonus in bonuses:
            matching_bonus = bonus[self.attrib_enum]
            if matching_bonus:
                attr += matching_bonus
        return attr.value()
