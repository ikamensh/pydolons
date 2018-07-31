import networkx as nx
import random
import numpy as np
from collections import namedtuple

G=nx.gnp_random_graph(4,0.2,directed=True)

# DAG = nx.DiGraph([(u,v,{'weight':random.randint(-10,10)}) for (u,v) in G.edges() if u<v])
# G = nx.Graph()


w = 40
h = 30
the_map = np.chararray([w, h])
the_map[:] = 'x'

area = w*h

n_rooms = len(G.nodes)

boxes = {}
Box = namedtuple("Box","x1 x2 y1 y2")

def gen_random_box(w,h):
    x1, y1 = random.randint(0,w), random.randint(0,h)
    x2, y2 = x1 + random.randint(2,w/2), y1 + random.randint(2,h/2)

    while x2 >= w or y2 >= h:
        x1, y1 = random.randint(0, w), random.randint(0, h)
        x2, y2 = x1 + random.randint(2, w / 2), y1 + random.randint(2, h / 2)

    return Box(x1,x2,y1,y2)


def check_crossection(bxs):
    result = False
    for b1 in bxs:
        for b2 in bxs:
            if b1 is b2:
                continue

            if b2.y1 <= b1.y1 <= b2.y2:
                return True
            elif b1.y1 <= b2.y1 <= b1.y2:
                return True

            if b2.x1 <= b1.x1 <= b2.x2:
                return True
            elif b1.x1 <= b2.x1 <= b1.x2:
                return True

    return result

for node in G.nodes:
    boxes[node] = gen_random_box(w, h)

n_tries = 0
while check_crossection(boxes.values()):
    n_tries += 1
    print(n_tries)
    for node in G.nodes:
        boxes[node] = gen_random_box(w, h)

def onto_map(boxes):
    for b in boxes:
        the_map[b.x1:b.x2, b.y1:b.y2] = '.'
        print(the_map[b.x1, b.y1])


onto_map(boxes.values())

with open('temp.txt', 'w') as fp:
    for row in range(the_map.shape[0]):
        fp.write( the_map[row].tobytes().decode("utf-8") + '\n')





