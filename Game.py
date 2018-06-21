from battlefield.Battlefield import Battlefield, Coordinates

class Game:
    def __init__(self, dungeon, hero):

        self.battlefield = Battlefield(dungeon.h, dungeon.w)
        self.battlefield.place_many(dungeon.units_locations)
        self.battlefield.place(hero, dungeon.hero_entrance)

        self.the_hero = hero

    def print_all_units(self):
        for unit, xy in self.battlefield.unit_locations.items():
            x, y = xy
            print("There is a {} at ({},{})".format(unit, x, y))

    def order_move(self, unit, p):
        # units can only go to adjecent locations
        if not self.battlefield.distance_unit_to_point(unit, p) <= 1:
            return False

        if p in self.battlefield.units:
            target = self.battlefield.units[p]
            self.attack(unit, target)
        else:
            self.battlefield.move(unit, p)

    def attack(self, attacker, target):
        damage = attacker.get_unarmed_damage()
        target.recieve_damage(damage)

    def __repr__(self):
        return "{} by {} dungeon with {} units in it.".format(self.battlefield.h, self.battlefield.w, len(self.battlefield.units))

    def loop(self):
        while True:
            orders = input("Tell me where to go!")
            x, y = [int(coord) for coord in orders.split()]
            print(x,y)
            self.order_move(self.the_hero, Coordinates(x,y))
            self.print_all_units()