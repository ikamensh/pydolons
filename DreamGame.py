from battlefield.Battlefield import Battlefield, Cell
from mechanics.turns import AtbTurnsManager
from mechanics.fractions import Fractions
from mechanics.AI import AstarAI, RandomAI
from mechanics.actives import CellTargeting, SingleUnitTargeting
import copy
import my_globals


class DreamGame:

    def __init__(self, bf):
        self.battlefield = bf
        self.the_hero = None
        self.fractions = {}
        self.brute_ai = AstarAI(bf, self.fractions)
        self.random_ai = RandomAI(bf)
        self.turns_manager = AtbTurnsManager()
        my_globals.the_game = self

    @staticmethod
    def start_dungeon(dungeon, hero):

        unit_locations = dungeon.unit_locations
        unit_locations = copy.deepcopy(unit_locations)
        unit_locations[hero] = dungeon.hero_entrance
        bf = Battlefield(dungeon.h, dungeon.w)
        game = DreamGame(bf)
        if unit_locations:
            bf.place_many(unit_locations)
        game.the_hero = hero

        game.fractions.update({unit:Fractions.ENEMY for unit in unit_locations if not unit.is_obstacle})
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

    @staticmethod
    def order_move(unit, target_cell, AI_assist=False):

        actives = unit.movement_actives
        if len(actives) == 0:
            return False, "The unit has no movement actives."

        tgt = CellTargeting(cell=target_cell)
        valid_actives = [a for a in actives if a.targeting_cond(tgt)]

        if len(valid_actives) == 0:
            # if AI_assist:
            #TODO instead of moving, turn towards the desired cell


            return False, "None of the user movement actives can reach the target cell."

        chosen_active = min(valid_actives, key=DreamGame.cost_heuristic(unit))
        chosen_active.activate(tgt)

        return True, chosen_active

    @staticmethod
    def order_attack(unit, target):
        actives = unit.attack_actives
        if len(actives) == 0:
            return False, "The unit has no attack actives."

        tgt = SingleUnitTargeting(unit=target)
        valid_actives = [a for a in actives if a.targeting_cond(tgt)]

        if len(valid_actives) == 0:
            return False, "None of the user attack actives can reach the target."

        chosen_active = min(valid_actives, key=DreamGame.cost_heuristic(unit))
        chosen_active.activate(tgt)

        return True, chosen_active

    @staticmethod
    def cost_heuristic(unit, factors = None):
        _factors = factors or {}

        def _(active):
            cost = active.cost
            hp_relative_cost = cost.health / unit.health * _factors.get("hp", 1)
            mana_relative_cost = cost.mana / unit.mana * _factors.get("hp", 0.5)
            stamina_relative_cost = cost.stamina / unit.stamina * _factors.get("hp", 0.5)
            readiness_cost = cost.readiness * _factors.get("rdy", 0.1)

            return sum( (hp_relative_cost, mana_relative_cost, stamina_relative_cost, readiness_cost) )

        return _





    @staticmethod
    def get_location(unit):
        assert unit in my_globals.the_game.battlefield.unit_locations
        return my_globals.the_game.battlefield.unit_locations[unit]

    def print_all_units(self):
        for unit, cell in self.battlefield.unit_locations.items():
            x, y = cell.x, cell.y
            print("There is a {} at ({},{})".format(unit, x, y))

    @staticmethod
    def get_unit_at(coord):
        return my_globals.the_game.battlefield.units_at[coord]

    @staticmethod
    def get_units_distances_from(p):
        return my_globals.the_game.battlefield.get_units_dists_to(p)

