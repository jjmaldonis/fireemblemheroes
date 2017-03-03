

class Simulator(object):
    def __init__(self, hero1, hero2, reset=True):
        self.hero1 = hero1
        self.hero2 = hero2
        self._turn = 1

        if reset:
            self.hero1.reset()
            self.hero2.reset()

    def run_turn(self):
        self._turn += 1
        print("{hero} attacks!".format(hero=self.hero1.name))
        self.hero1.attack_target(self.hero2)
        if self.hero2.weapon.range == self.hero1.weapon.range:  # return attack
            print("{hero} attacks in return!".format(hero=self.hero2.name))
            self.hero2.attack_target(self.hero1)


        if self.hero2.stats.current_hp <= 0:
            return  # early

        print("{hero} attacks!".format(hero=self.hero2.name))
        self.hero2.attack_target(self.hero1)
        if self.hero1.weapon.range == self.hero2.weapon.range:  # return attack
            print("{hero} attacks in return!".format(hero=self.hero1.name))
            self.hero2.attack_target(self.hero1)

    def run(self):
        print("Running simulation with {} and {}...".format(self.hero1, self.hero2))
        while self.hero1.stats.current_hp > 0 and self.hero2.stats.current_hp > 0:
            print("Turn", self._turn)
            self.run_turn()
        print()
        print("Finished simulation on turn {}.".format(self._turn - 1))
        print("{hero} has {hp} ({percent}%) hp remaining.".format(hero=self.hero1.name, hp=self.hero1.stats.current_hp, percent=max(0,int(round(100*self.hero1.stats.current_hp/self.hero1.stats.hp)))))
        print("{hero} has {hp} ({percent}%) hp remaining.".format(hero=self.hero2.name, hp=self.hero2.stats.current_hp, percent=max(0,int(round(100*self.hero2.stats.current_hp/self.hero2.stats.hp)))))

    @property
    def state(self):
        return GameState(hero1=self.hero1, hero2=self.hero2, turn=self._turn)


class GameState(object):
    def __init__(self, hero1, hero2, turn):
        self.hero1 = hero1
        self.hero2 = hero2
        self.turn = turn

