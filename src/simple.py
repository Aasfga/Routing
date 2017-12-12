import logging

from routing.algorithms import ShortPathRouter, GraphVector
from routing.simulator import Simulator

logging.basicConfig(level=logging.DEBUG)
sim = Simulator()
# ShortPathRouter.set_vector(SimpleVector)
ShortPathRouter.set_vector(GraphVector)
algo = ShortPathRouter
r1 = sim.add_router(algo, 'a')
r2 = sim.add_router(algo, 'b')
r3 = sim.add_router(algo, 'c')
r4 = sim.add_router(algo, 'd')
r5 = sim.add_router(algo, 'e')
r6 = sim.add_router(algo, 'f')
r7 = sim.add_router(algo, 'g')
r8 = sim.add_router(algo, 'h')
r9 = sim.add_router(algo, 'i')
sim.add_link(r1, r2)
sim.add_link(r2, r3)
sim.add_link(r3, r4)
sim.add_link(r4, r5)
sim.add_link(r5, r6)
sim.add_link(r6, r7)
sim.add_link(r7, r8)
sim.add_link(r8, r9)


for i in range(2000):
    if i % 3 == 0:
        sim.add_packet(r1, r9)
    sim.route()

for i in range(30):
    sim.route()
print(sim.stats)
