#TODO this class is not used? delete?

class CharacterModel(object):
    """docstring for CharacterModel."""
    def __init__(self):
        super(CharacterModel, self).__init__()
        self.baseType =  BaseType({'str':45, 'agi': 15,'prc': 15}, "Demo Hero", icon="hero.png")
        self.character = Character(self.baseType)
        self.printCharacter(self.character)
        print('self.character dir :\n',dir(self.character))
        self.the_hero = None
        self.data = {}

    def printCharacter(self, char):
        print('char.xp_total = ',char.xp_total)
        print('char.preliminary_attributes = ',char.preliminary_attributes)
        print('char.preliminary_masteries = ',char.preliminary_masteries)
        print('char.masteries_can_go_up = ',char.masteries_can_go_up)
        print('char.attributes_count = ',char.attributes_count)
        print('char.free_attribute_points = ',char.free_attribute_points)
        print('char.free_xp = ',char.free_xp)
        print('char.increase_attrib = ',char.increase_attrib)
        # print('char.base_type_prelim = ',char.base_type_prelim)
        # print('char.unit = ',char.unit)

    def setHero(self, hero):
        self.the_hero = hero
        self.update()

    def update(self):
        self.printCharacter(self.character)
        self.data['hp'] = self.the_hero.health
        self.data['max_hp'] = self.the_hero.max_health
        self.data['mana'] = self.the_hero.mana
        self.data['max_mana'] = self.the_hero.max_mana
        self.data['stamina'] = self.the_hero.stamina
        self.data['max_stamina'] = self.the_hero.max_stamina
