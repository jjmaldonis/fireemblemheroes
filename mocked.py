import json

from simulator.hero import all_heroes
from simulator.simulator import Simulator


#hero1 = all_heroes["Nino"]
#hero2 = all_heroes["Lucina"]
hero1 = all_heroes["Robin (M)"]
hero2 = all_heroes["Takumi"]
#hero1.stats.attack = 20
#hero2.stats.attack = 20


print(hero1)
print(hero1.stats)
print(hero1.skills)
print()
print(hero2)
print(hero2.stats)
print(hero2.skills)
print()
print()

sim = Simulator(hero1, hero2)
sim.run()

print()
print()

sim = Simulator(hero2, hero1)
sim.run()
