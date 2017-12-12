# Routing - small network simulator


Small simulator that uses RIP protocol 
to share network map between routers.


To use simulator you have to create routers 
and links between them. You also have to specify
routing algorithm (for short path algorithm you also 
have to specify vector class )
I have writen vector classes and short path algorithm. 
Everything else was provided by lecturer


# Examples
```
ShortPathRouter.set_vector(GraphVector)    
#set vector class

sim = Simulator()
algo = ShortPathRouter
v = sim.add_router(algo, 'a')
u = sim.add_router(algo, 'b')
sim.add_link(u, v)
#add router and link

for i in range(100):
    if i % 2 == 0:
        sim.add_packet(u, v)
    sim.route()
#simple simulation
#more examples in src folder

``` 
