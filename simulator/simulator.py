

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
        self.phase_one()
        if self.hero1.current_hp <= 0 or self.hero2.current_hp <= 0:
            return  # early
        self.phase_two()

    def phase_one(self):
        print("{hero} attacks! (Phase 1)".format(hero=self.hero1.name))
        self.hero1.attack_target(self.hero2)
        if self.hero2.current_hp > 0 and self.hero2.can_counterattack(self.hero1):
            print("{hero} counterattacks!".format(hero=self.hero2.name))
            self.hero2.attack_target(self.hero1)

    def phase_two(self):
        print("{hero} attacks! (Phase 2)".format(hero=self.hero2.name))
        self.hero2.attack_target(self.hero1)
        if self.hero1.current_hp > 0 and self.hero1.can_counterattack(self.hero1):
            print("{hero} counterattacks!".format(hero=self.hero1.name))
            self.hero1.attack_target(self.hero2)

    def run(self):
        print("Running simulation with {} and {}...".format(self.hero1, self.hero2))
        while self.hero1.stats.current_hp > 0 and self.hero2.stats.current_hp > 0:
            print("Turn", self._turn)
            self.run_turn()
        winner = self.hero1 if self.hero1.current_hp > 0 else self.hero2
        print()
        print("Finished simulation on turn {}. {} won!".format(self._turn - 1, winner))
        print("{hero} has {hp} ({percent}%) hp remaining.".format(hero=self.hero1.name, hp=self.hero1.stats.current_hp, percent=max(0,int(round(100*self.hero1.stats.current_hp/self.hero1.stats.hp)))))
        print("{hero} has {hp} ({percent}%) hp remaining.".format(hero=self.hero2.name, hp=self.hero2.stats.current_hp, percent=max(0,int(round(100*self.hero2.stats.current_hp/self.hero2.stats.hp)))))
        return winner

    @property
    def state(self):
        return GameState(hero1=self.hero1, hero2=self.hero2, turn=self._turn)


class GameState(object):
    def __init__(self, hero1, hero2, turn):
        # Do we need more stuff here? What else is there?
        self.hero1 = hero1
        self.hero2 = hero2
        self.turn = turn

