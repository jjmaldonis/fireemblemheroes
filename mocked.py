import json

from simulator.hero import all_heroes
from simulator.simulator import Simulator


nino = all_heroes["Nino"] #Hero.from_json(filename=os.path.join(cwd, "data/nino.json"))
lucina = all_heroes["Lucina"] #Hero.from_json(filename=os.path.join(cwd, "data/lucina.json"))

print(nino)
print(nino.stats)
print(nino.skills)

print()

print(lucina)
print(lucina.stats)
print(lucina.skills)

print()
print()

sim = Simulator(nino, lucina)
sim.run()

print()
print()

sim = Simulator(lucina, nino)
sim.run()
