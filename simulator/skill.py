

class Skill(object):
    # This is not even close to fully implemented. Not sure how we are going to do that yet.
    def __init__(self, name, stat_modifier=None, countdown=None, description="", use_on_offense=False, use_on_defense=False, permanent=False):
        from .hero import Buff
        global Buff
        self.name = name
        self.stat_modifier = stat_modifier
        self.countdown = countdown
        self.description=description
        self.use_on_offense = use_on_offense
        self.use_on_defense = use_on_defense
        self.permanent = permanent

        self.max_countdown = countdown
        self.hero = None
        self.reset()

    def __str__(self):
        return self.name
    __repr__ = __str__

    @property
    def ready(self, game_state=None):
        return self.countdown is not None and self.countdown == 0

    def reset(self):
        self.countdown = self.max_countdown
        #if self.hero and self.stat_modifier in self.hero.buffs_this_combat:
        #    self.hero.buffs_this_combat.remove(self.stat_modifier)

    def decrement(self):
        if self.countdown is not None and self.countdown > 0:
            self.countdown -= 1

    # Abstract method?
    def use(self, user, target):
        print(f"  {self.hero.name} is using {self.name}!", self.stat_modifier)
        self.reset()
        return self.stat_modifier

    def bind_to_hero(self, hero):
        self.hero = hero





class Resistance(Skill):
    def __init__(self):
        super().__init__(name="Resistance +3", stat_modifier=Buff(hp=0, attack=0, speed=0, defense=0, resistance=3),
            countdown=None, description="Grants Res +3.", permanent=True)

class SpurDefense(Skill):  # TODO Don't know how we would apply this as a permanent buff.
    def __init__(self):
        super().__init__(name="Spur Defense 3", stat_modifier=None, countdown=0, description="Grants adjacent friendly unit's Defense+3 during combat.", use_on_offense=True, use_on_defense=True)

    @property
    def ready(self, game_state=None):
        return False

class SpurAttack(Skill):  # TODO Don't know how we would apply this as a permanent buff.
    def __init__(self):
        super().__init__(name="Spur Attack 3", stat_modifier=None, countdown=0, description="Grants adjacent friendly unit's Attack+3 during combat.", use_on_offense=True, use_on_defense=True)

    @property
    def ready(self, game_state=None):
        return False

class ThreatenSpeed(Skill):  # TODO Don't know how to apply this.
    def __init__(self):
        super().__init__(name="Threaten Speed 3", stat_modifier=None, countdown=0, description="Inflicts Speed-5 on enemies within 2 spaces through their next actions at the start of each turn.")

    @property
    def ready(self, game_state=None):
        return False

class DefiantSpeed(Skill):
    def __init__(self):
        super().__init__(name="Defiant Speed 3", stat_modifier=None, countdown=0, description="Grants Speed+7 at start of turn if character's Health Points ≤ 50%.", use_on_offense=True, use_on_defense=True)

    @property
    def ready(self, game_state=None):
        return self.hero.current_hp <= self.hero.hp / 2

    def use(self, user, target):
        self.stat_modifier = Buff(hp=0, attack=0, speed=7, defense=0, resistance=0)
        user.buffs_this_combat.append(self.stat_modifier)
        return super().use(user, target)

class CloseCounter(Skill):
    def __init__(self):
        super().__init__(name="Close Counter", stat_modifier=None, countdown=None, description="Allows character to counter attack regardless of distance to attacker.")

class DistantCounter(Skill):
    def __init__(self):
        super().__init__(name="Distant Counter", stat_modifier=None, countdown=None, description="Allows character to counter attack regardless of distance to attacker.")

class Luna(Skill):
    def __init__(self):
        super().__init__(name="Luna", stat_modifier=None, countdown=3, description="Resolve combat as if foe suffered Def/Res -50%.", use_on_offense=True)

    def use(self, user, target):
        self.stat_modifier = Buff(hp=0, attack=0, speed=0, defense=-target.stats.defense/2, resistance=-target.stats.resistance/2)
        target.buffs_this_combat.append(self.stat_modifier)
        return super().use(user, target)

class Bonfire(Skill):
    def __init__(self):
        super().__init__(name="Bonfire", stat_modifier=None, countdown=3, description="Boosts damage dealt by 50% of character's Defense.", use_on_offense=True)

    def use(self, user, target):
        self.stat_modifier = Buff(hp=0, attack=user.defense/2, speed=0, defense=0, resistance=0)  # TODO This might have a small bug if a defense-boosting skill is added after this one.
        user.buffs_this_combat.append(self.stat_modifier)
        return super().use(user, target)

class Vengeance(Skill):
    def __init__(self):
        super().__init__(name="Vengence", stat_modifier=None, countdown=3, description="Grants bonus to damage dealt equal to 50% of damage suffered.", use_on_offense=True)

    def use(self, user, target):
        bonus = int( (user.hp - user.current_hp) / 2 )
        self.stat_modifier = Buff(hp=0, attack=bonus, speed=0, defense=0, resistance=0)
        user.buffs_this_combat.append(self.stat_modifier)
        return super().use(user, target)


all_skills = {"Luna": Luna,
              "Defiant Speed 3": DefiantSpeed,
              "Bonfire": Bonfire,
              "Spur Defense 3": SpurDefense,
              "Spur Attack 3":SpurAttack,
              "Resistance +3": Resistance,
              "Vengeance": Vengeance,
              "Close Counter": CloseCounter,
              "Distant Counter": DistantCounter,
              "Threaten Speed 3": ThreatenSpeed
}

