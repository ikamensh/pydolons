import functools

class MyVision:
    counter = 0

    @functools.lru_cache(maxsize=int(2**24))
    def my_dummy_calc(self, x, y, z):
        if x.x > y.x:
            return self.my_dummy_calc(y, x, z)
        self.counter+=1
        return x

from collections import namedtuple

quack = namedtuple("quack", "x y")

m = MyVision()

quacks = []
for i in range(8):
    for j in range(8):
        quacks.append( quack(i,j) )

for q1 in quacks:
    for q2 in quacks:
        for q3 in quacks:
            m.my_dummy_calc(q1, q2, q3)
            m.my_dummy_calc(q2, q1, q3)

print(m.counter)



