import random
import logging
from routing.algorithms import ShortPathRouter, GraphVector
from routing.simulator import Simulator

logging.basicConfig(level=logging.DEBUG)
sim = Simulator()
# ShortPathRouter.set_vector(SimpleVector)
ShortPathRouter.set_vector(GraphVector)
algo = ShortPathRouter
a_list = [sim.add_router(algo, 'a1'),
          sim.add_router(algo, 'a2'),
          sim.add_router(algo, 'a3'),
          sim.add_router(algo, 'a4'),
          sim.add_router(algo, 'a5'),
          sim.add_router(algo, 'a6')
          ]
b_list = [sim.add_router(algo, 'b1'),
          sim.add_router(algo, 'b2'),
          sim.add_router(algo, 'b3'),
          sim.add_router(algo, 'b4'),
          sim.add_router(algo, 'b5'),
          sim.add_router(algo, 'b6')
          ]
sim.add_link(a_list[0], a_list[1])
sim.add_link(a_list[1], a_list[2])
sim.add_link(a_list[2], a_list[3])
sim.add_link(a_list[3], a_list[4])
sim.add_link(a_list[4], a_list[5])
sim.add_link(a_list[5], a_list[0])

sim.add_link(b_list[0], b_list[1])
sim.add_link(b_list[1], b_list[2])
sim.add_link(b_list[2], b_list[3])
sim.add_link(b_list[3], b_list[4])
sim.add_link(b_list[4], b_list[5])
sim.add_link(b_list[5], b_list[0])

random.shuffle(a_list)
random.shuffle(b_list)
sim.add_link(b_list[0], a_list[0])
sim.add_link(b_list[5], a_list[5])

for i in range(3000):
    random.shuffle(a_list)
    random.shuffle(b_list)
    if i % 3 == 0:
        sim.add_packet(a_list[0], b_list[0])
    sim.route()

for i in range(30):
    sim.route()


s = sim.stats

print(s)

