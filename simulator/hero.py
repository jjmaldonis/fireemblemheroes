import os
import enum
import json

from .weapons import all_weapons, DamageType


class UnitType(enum.Enum):
    CAVALRY = "Cavalry"
    INFANTRY = "Infantry"
    FLYING = "Flying"
    DRAGON = "Dragon"
    ARMORED = "Armored"
    # The below are all Infantry not types of units; their weapon type defines them beyond Infantry
    #DAGGER = "Dagger"
    #HEALER = "Healer"
    #ARCHER = "Archer"
    # More?


class StatType(enum.Enum):
    HP = "hp"
    ATTACK = "attack"
    SPEED = "speed"
    DEFENSE = "defense"
    RESISTANCE = "resistance"


class Stats(object):
    def __init__(self, hp, attack, speed, defense, resistance):
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.defense = defense
        self.resistance = resistance

        self.current_hp = self.hp

    @classmethod
    def from_json(cls, data):
        return cls(**data)
        #return cls(data["hp"], data["attack"], data["speed"], data["defense"], data["resistance"])

    def __str__(self):
        return "<HP:{}, ATK:{}, SPD:{}, DEF:{}, RES:{}>".format(
            self.hp, self.attack, self.speed, self.defense, self.resistance
        )
    __repr__ = __str__


class Buff(Stats):
    # This just inherits Stats, and we can set the +- values using the same format.
    pass


class Skill(object):
    # This is not even close to fully implemented. Not sure how we are going to do that yet.
    def __init__(self, name, stat_modifier=None, countdown=None):
        self.name = name
        self.countdown = countdown
        self.stat_modifier = stat_modifier

        self.max_countdown = countdown
        self.reset()

    def __str__(self):
        return self.name
    __repr__ = __str__

    def ready(self, game_state):
        return countdown is not None and self.countdown == 0

    def reset(self):
        self.countdown = self.max_countdown

    def decrement(self):
        if countdown is not None:
            self.countdown -= 1

    def apply(self):
        self.reset()
        return self.stat_modifier


class Hero(object):
    def __init__(self, name, unit_type, stats, weapon, skills, strength=None, weakness=None):
        self.name = name
        self.unit_type = unit_type
        self.stats = stats
        self.weapon = weapon
        self.skills = skills

        self.buffs = []  # buffs get added / removed manually

        # TODO For now, assume all bonuses/penalties are +- 3 only even tho that's not true
        if strength is not None:
            setattr(stats, strength.value,
                getattr(stats, strength.value) + 3
            )
        if weakness is not None:
            setattr(stats, weakness.value,
                getattr(stats, weakness.value) + 3
            )

    @classmethod
    def from_json(cls, data=None, filename=None, strength=None, weakness=None):
        if filename:
            data = json.load(open(filename))
        else:
            assert data is not None

        name = data["name"]
        stats = Stats.from_json(data["stats"])
        unit_type = UnitType(data["unit_type"])
        weapon = all_weapons[data["weapon"]]
        skills = [Skill(skill) for skill in data["skills"]]

        return cls(name=name, stats=stats, unit_type=unit_type, weapon=weapon, skills=skills, strength=strength, weakness=weakness)

    def __str__(self):
        return self.name
    __repr__ = __str__

    def calculate_damage(self, hero):
        damage = self.attack
        if self.weapon.damage_type == DamageType.PHYSICAL:
            damage -= hero.stats.defense
        elif self.weapon.damage_type == DamageType.MAGIC:
            damage -= hero.stats.resistance
        # apply weapon triangle  (is it +3 damage?) TODO
        if self.weapon > hero.weapon:
            damage += 3
        elif self.weapon < hero.weapon:
            damage -= 3
        return damage

    def attack_target(self, hero):
        damage = self.calculate_damage(hero)
        hero.apply_damage(damage)
        # apply speed
        if self.stats.speed - hero.stats.speed > 5:
            print("Double attack!")
            hero.apply_damage(damage)
        # Also decrement self's trigger countdown when self does damage
        return damage

    def apply_damage(self, damage):
        self.stats.current_hp -= damage
        # Also decrement self's trigger countdown when self takes damage
        return self.stats.current_hp

    def add_buff(self, buff):
        self.buffs.append(buff)

    def remove_buff(self, buff):
        self.buffs.remove(buff)

    @property
    def hp(self):
        return self.stats.hp + sum(buff.hp for buff in self.buffs)

    @property
    def attack(self):
        return self.stats.attack + sum(buff.attack for buff in self.buffs)

    @property
    def speed(self):
        return self.stats.speed + sum(buff.speed for buff in self.buffs)

    @property
    def defense(self):
        return self.stats.defense + sum(buff.defense for buff in self.buffs)

    @property
    def resistance(self):
        return self.stats.resistance + sum(buff.resistance for buff in self.buffs)

    def reset(self):
        """Resets the hero for a new simulation."""
        self.stats.current_hp = self.stats.hp
        self.buffs = []


# Load all the heros in the data directory
cwd, _ = os.path.split(__file__)
data_dir = os.path.join(cwd, "..", "data")
all_heroes = [Hero.from_json(filename=os.path.join(data_dir, filename)) for filename in os.listdir(data_dir)]
all_heroes = {hero.name: hero for hero in all_heroes}

