import functools

class MyVision:
    counter = 0

    @functools.lru_cache(maxsize=int(2**8))
    def my_dummy_calc(self, x, y, z):
        if x.x > y.x:
            return self.my_dummy_calc(y, x, z)
        self.counter+=1
        return x

from collections import namedtuple

quack = namedtuple("quack", "x y")

m = MyVision()

quacks = list()
for i in range(8):
    for j in range(8):
        quacks.append( quack(i,j) )

import random

results = []

qs = quacks[:5]

while len(results) < 500_000:
    if random.random() < 0.9:
        q1 = random.choice(qs)
        q2 = random.choice(qs)
        q3 = random.choice(qs)

    else:
        q1 = random.choice(quacks)
        q2 = random.choice(quacks)
        q3 = random.choice(quacks)

    results.append(m.my_dummy_calc(q1,q2,q3))

print(m.counter)



