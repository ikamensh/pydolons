

class Dungeon:
    def __init__(self, name, h, w, *, unit_locations, hero_entrance, icon="dungeon.png"):

        self.name = name

        self.unit_locations = unit_locations
        self.h = h
        self.w = w
        self.hero_entrance = hero_entrance

        self.icon = icon

