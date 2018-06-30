from battlefield.Battlefield import Battlefield, Coordinates
from mechanics.damage import deal_damage
from mechanics.combat import Attack

class DreamGame:
    the_game = None

    def __init__(self, bf):
        self.battlefield = bf
        DreamGame.the_game = self

    @staticmethod
    def start_dungeon(dungeon, hero):

        DreamGame(Battlefield(dungeon.h, dungeon.w))
        DreamGame.the_game.battlefield.place_many(dungeon.units_locations)
        DreamGame.the_game.battlefield.place(hero, dungeon.hero_entrance)
        DreamGame.the_game.the_hero = hero
        return DreamGame.the_game


    @staticmethod
    def custom_init(bf):
        DreamGame(bf)

    @staticmethod
    def get_unit_at(coord):
        return DreamGame.the_game.battlefield.units_at[coord]

    @staticmethod
    def get_units_distances_from(p):
        return DreamGame.the_game.battlefield.get_units_sorted_by_proximity_to()

    def print_all_units(self):
        for unit, xy in self.battlefield.unit_locations.items():
            x, y = xy
            print("There is a {} at ({},{})".format(unit, x, y))

    def order_move(self, unit, p):
        # units can only go to adjecent locations
        if not self.battlefield.distance_unit_to_point(unit, p) <= 1:
            return False

        if p in self.battlefield.units_at:
            target = self.battlefield.units_at[p]
            self.attack(unit, target)
        else:
            self.battlefield.move(unit, p)
        return True


    def attack(self, attacker, target):
        target_died = Attack.attack(attacker, target)
        if target_died:
            self.battlefield.remove(target)

    @staticmethod
    def get_location(unit):
        assert unit in DreamGame.the_game.battlefield.unit_locations
        return DreamGame.the_game.battlefield.unit_locations[unit]


    def __repr__(self):
        return "{} by {} dungeon with {} units in it.".format(self.battlefield.h, self.battlefield.w, len(self.battlefield.units_at))

    def loop(self):
        while True:
            orders = input("Tell me where to go!")
            x, y = [int(coord) for coord in orders.split()]
            print(x,y)
            self.order_move(self.the_hero, Coordinates(x,y))
            self.print_all_units()