from game_objects.battlefield_objects import base_attributes, enum_to_abbrev


class GameHeroAttr:
    def __init__(self, character, gameRoot):
        self.gameRoot = gameRoot
        self.character = character
        self.attrs = {}
        self.attrs_info = {}
        self.setUpHeroAttr()

    def setUpHeroAttr(self):
        self.attrs = {v: k for k, v in enum_to_abbrev.items()}
        self.attrs_info = {
            'cha_' + name: attr.tooltip_info for name,
            attr in self.attrs.items()}
        self._free_xp = self.free_xp

    def freePointsChanged(self, value, attr):
        if self.character.temp_attributes is None:
            attributes = self.character.base_type.attributes
        else:
            attributes = self.character.temp_attributes

        if attributes[attr] == value:
            return
        elif attributes[attr] > value:
            self.character.reduce_attrib(attr)
        else:
            self.character.increase_attrib(attr)
            if self.character.free_attribute_points == 0:
                vl = attributes[attr]

    def attr_up(self, attr):
        self.character.increase_attrib(attr)

    def attr_down(self, attr):
        if self._free_xp > self.free_xp:
            self.character.reduce_attrib(attr)

    def attr_value(self, attr):
        if self.character.temp_attributes is None:
            attributes = self.character.base_type.attributes
        else:
            attributes = self.character.temp_attributes
        return str(attributes[attr])

    @property
    def health(self):
        return str(self.gameRoot.lengine.the_hero.health)

    @property
    def max_health(self):
        return str(self.gameRoot.lengine.the_hero.max_health)

    @property
    def mana(self):
        return str(self.gameRoot.lengine.the_hero.mana)

    @property
    def max_mana(self):
        return str(self.gameRoot.lengine.the_hero.max_mana)

    @property
    def stamina(self):
        return str(self.gameRoot.lengine.the_hero.stamina)

    @property
    def max_stamina(self):
        return str(self.gameRoot.lengine.the_hero.max_stamina)

    @property
    def free_xp(self):
        return str(self.character.free_attribute_points)

    def reset_all(self):
        self.character.reset()

    def commit_changes(self):
        self._free_xp = self.free_xp
        try:
            self.character.commit()
        except Exception as er:
            print("D'ont commit character", er)

    @property
    def hero_icon(self):
        return self.gameRoot.lengine.the_hero.icon
