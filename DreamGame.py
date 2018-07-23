from battlefield.Battlefield import Battlefield, Cell
from mechanics.combat import Attack
from mechanics.turns import AtbTurnsManager
from mechanics.fractions import Fractions
from mechanics.AI import AstarAI, RandomAI
from battlefield.MovementEvent import MovementEvent
import my_globals


class DreamGame:

    def __init__(self, bf, unit_locations = None):
        self.battlefield = bf
        self.the_hero = None
        self.fractions = {}
        self.brute_ai = AstarAI(bf, self.fractions)
        self.random_ai = RandomAI(bf)
        self.turns_manager = AtbTurnsManager()
        my_globals.the_game = self

        if unit_locations:
            bf.place_many(unit_locations)



    @staticmethod
    def start_dungeon(dungeon, hero):

        unit_locations = dungeon.unit_locations
        unit_locations[hero] = dungeon.hero_entrance

        game = DreamGame(Battlefield(dungeon.h, dungeon.w), unit_locations)
        game.the_hero = hero

        game.fractions.update({unit:Fractions.ENEMY for unit in dungeon.unit_locations if not unit.is_obstacle})
        game.fractions[hero] = Fractions.PLAYER

        units_who_make_turns = [unit for unit in unit_locations.keys()
                                if not unit.is_obstacle]
        game.turns_manager = AtbTurnsManager(units_who_make_turns)

        return game

    def add_unit(self, unit, cell,  fraction):
        self.fractions[unit] = fraction
        self.battlefield.place(unit, cell)
        self.turns_manager.add_unit(unit)

    def unit_died(self, unit):
        del self.fractions[unit]
        self.battlefield.remove(unit)
        self.turns_manager.remove_unit(unit)
        unit.alive = False

    def obstacle_destroyed(self, obstacle):
        self.battlefield.remove(obstacle)

    def add_obstacle(self, obstacle, cell):
        self.battlefield.place(obstacle, cell)

    def loop(self, player_berserk=False):
        count_hero_turns = 0
        while True:
            active_unit = self.turns_manager.get_next()
            target_cell = None
            if self.fractions[active_unit] is Fractions.PLAYER:
                count_hero_turns += 1
                if player_berserk:
                    target_cell=self.brute_ai.decide_step(active_unit, target_fraction=Fractions.ENEMY)
                else:
                    orders = input("Tell me where to go!")
                    x, y = [int(coord) for coord in orders.split()]
                    print(x,y)
                    target_cell = Cell(x, y)

            elif self.fractions[active_unit] is Fractions.ENEMY:
                target_cell = self.brute_ai.decide_step(active_unit)
            elif self.fractions[active_unit] is Fractions.NEUTRALS:
                target_cell = self.random_ai.decide_step(active_unit)

            self.order_move(active_unit, target_cell)
            game_over = self.game_over()
            if game_over:
                print(game_over)
                return count_hero_turns
            # self.print_all_units()

    def game_over(self):
        own_units = [unit for unit in self.fractions if self.fractions[unit] is Fractions.PLAYER]
        enemy_units = [unit for unit in self.fractions if self.fractions[unit] is Fractions.ENEMY]

        if len(own_units) == 0:
            return "DEFEAT"
        elif len(enemy_units) == 0:
            return "VICTORY"
        else:
            return None

    def __repr__(self):
        return "{} by {} dungeon with {} units in it.".format(self.battlefield.h, self.battlefield.w, len(self.battlefield.units_at))

    def order_move(self, unit, target_cell):
        # TODO refactor with actives and their conditions?
        # units can only go to adjecent locations
        if not self.battlefield.distance(unit, target_cell) <= 1:
            return False

        if target_cell in self.battlefield.units_at:
            target = self.battlefield.units_at[target_cell]
            self.attack(unit, target)
        else:
            MovementEvent(self.battlefield, unit, target_cell)

        return True


    @staticmethod
    def get_location(unit):
        assert unit in my_globals.the_game.battlefield.unit_locations
        return my_globals.the_game.battlefield.unit_locations[unit]

    def print_all_units(self):
        for unit, xy in self.battlefield.unit_locations.items():
            x, y = xy
            print("There is a {} at ({},{})".format(unit, x, y))

    @staticmethod
    def attack(attacker, target):
        Attack.attack(attacker, target)

    @staticmethod
    def get_unit_at(coord):
        return my_globals.the_game.battlefield.units_at[coord]

    @staticmethod
    def get_units_distances_from(p):
        return my_globals.the_game.battlefield.get_units_dists_to(p)

