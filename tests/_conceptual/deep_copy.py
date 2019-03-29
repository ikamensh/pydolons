import copy


class Unit:
    counter = 0

    def __init__(self, friend, enemy):
        Unit.counter += 1
        self.friend = friend
        self.enemy = enemy
        print(f"{Unit.counter}th Unit created.")


class RelationshipDB:
    def __init__(self, units):
        self.units = units


a = Unit(None, None)
b = Unit(a, None)
c = Unit(b, a)

rl = RelationshipDB([a, b, c])


def my_printout(relationsDB):
    x = relationsDB.units[0]
    y = relationsDB.units[1]
    z = relationsDB.units[2]

    print(y.friend is x)
    print(z.friend is y)
    print(z.enemy is x)


my_printout(rl)


rl_2 = copy.deepcopy(rl)

my_printout(rl_2)
