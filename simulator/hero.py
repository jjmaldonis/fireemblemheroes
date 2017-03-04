import os
import enum
import json

from .weapons import all_weapons, DamageType, AddTotalBonusesToDamageDealt
from .skill import all_skills, Skill


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


class Hero(object):
    def __init__(self, name, unit_type, stats, weapon, skills, strength=None, weakness=None):
        self.name = name
        self.unit_type = unit_type
        self.stats = stats
        self.weapon = weapon
        weapon.bind_to_hero(self)
        self.skills = skills
        for skill in skills:
            skill.bind_to_hero(self)

        self.permanent_buffs = []  # buffs get added / removed manually
        self.buffs_this_combat = []  # includes Special Skill buffs (e.g. Luna)
        self.buffs_until_end_of_turn = []

        for skill in skills:
            if skill.permanent:
                self.permanent_buffs.append(skill.stat_modifier)

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
        skills = [all_skills[skill]() for skill in data["skills"] if skill in all_skills]

        return cls(name=name, stats=stats, unit_type=unit_type, weapon=weapon, skills=skills, strength=strength, weakness=weakness)

    def __str__(self):
        return self.name
    __repr__ = __str__

    def calculate_damage(self, hero):
        damage = self.attack
        if self.weapon.damage_type == DamageType.PHYSICAL:
            damage -= hero.defense
        elif self.weapon.damage_type == DamageType.MAGIC:
            damage -= hero.resistance

        # apply weapon triangle
        if self.has_advantage(hero):
            damage *= 1.2
        if self.has_disadvantage(hero):
            damage /= 1.2

        if isinstance(self.weapon.special, AddTotalBonusesToDamageDealt):
            damage += self.weapon.special.bonus_damage
        return damage

    def has_advantage(self, hero):
        if self.weapon > hero.weapon:
            return True

    def has_disadvantage(self, hero):
        if self.weapon < hero.weapon:
            return True

    def can_counterattack(self, hero):
        if self.weapon.range == hero.weapon.range or self.weapon.special.name == "Close Counter" or self.weapon.special.name == "Distant Counter":
            return True
        else:
            return False

    def attack_target(self, hero, is_second_attack=False):
        # Use special skills; this is done via stats objects in self.buffs_this_combat
        skills_used_this_attack = []
        for skill in self.skills:
            if skill.ready and skill.use_on_offense:
                stats = skill.use(user=self, target=hero)
                skills_used_this_attack = []

        damage = self.calculate_damage(hero)
        damage = int(damage)
        hero.take_damage(damage)

        # Tick any special skill countdowns
        for skill in self.skills:
            if skill not in skills_used_this_attack:
                skill.decrement()

        # apply speed;  what about brave weapons?
        if self.speed - hero.speed > 5 and not is_second_attack and hero.current_hp > 0:
            # Remove special skills and other temporary buffs; this needs to apply after the if statement
            self.buffs_this_combat.clear()
            print(f"{self.name} attacks a second time!")
            self.attack_target(hero, is_second_attack=True)
        else:
            # Remove special skills and other temporary buffs
            self.buffs_this_combat.clear()
        return damage

    def take_damage(self, damage):
        if damage < 0: damage = 0
        # Apply special skills; this is done via stats objects in self.buffs_this_combat
        skills_used_this_attack = []
        for skill in self.skills:
            if skill.ready and skill.use_on_defense:
                skill.use(user=self, target=None)
                skills_used_this_attack = []
        # Use skills
        self.stats.current_hp -= damage
        # Remove special skills
        self.buffs_this_combat.clear()
        # Tick any special skill countdowns
        for skill in self.skills:
            if skill not in skills_used_this_attack:
                skill.decrement()
        print(f"  {self.name} took {damage} damage ({self.current_hp} hp remaining)")
        return self.current_hp

    def add_buff(self, buff):
        self.permanent_buffs.append(buff)

    def remove_buff(self, buff):
        self.permanent_buffs.remove(buff)

    def add_temporary_buff(self, buff):
        self.buffs_this_combat.append(buff)

    def remove_temporary_buff(self, buff):
        self.buffs_this_combat.remove(buff)

    @property
    def bonus_hp(self):
        return sum(buff.hp for buff in self.permanent_buffs + self.buffs_this_combat)

    @property
    def bonus_attack(self):
        return sum(buff.attack for buff in self.permanent_buffs + self.buffs_this_combat)

    @property
    def bonus_speed(self):
        return sum(buff.speed for buff in self.permanent_buffs + self.buffs_this_combat)

    @property
    def bonus_defense(self):
        return sum(buff.defense for buff in self.permanent_buffs + self.buffs_this_combat)

    @property
    def bonus_resistance(self):
        return sum(buff.resistance for buff in self.permanent_buffs + self.buffs_this_combat)

    @property
    def hp(self):
        return self.stats.hp + self.bonus_hp

    @property
    def attack(self):
        return self.stats.attack + self.bonus_attack

    @property
    def speed(self):
        return self.stats.speed + self.bonus_speed

    @property
    def defense(self):
        return self.stats.defense + self.bonus_defense

    @property
    def resistance(self):
        return self.stats.resistance + self.bonus_resistance

    @property
    def current_hp(self):
        return self.stats.current_hp

    def reset(self):
        """Resets the hero for a new simulation."""
        self.stats.current_hp = self.hp
        for skill in self.skills:
            skill.reset()


# Load all the heros in the data directory
cwd, _ = os.path.split(__file__)
data_dir = os.path.join(cwd, "..", "data")
for filename in os.listdir(data_dir):
    try:
        Hero.from_json(filename=os.path.join(data_dir, filename))
    except:
        print("Failed to load {}".format(filename))
        raise
all_heroes = [Hero.from_json(filename=os.path.join(data_dir, filename)) for filename in os.listdir(data_dir)]
all_heroes = {hero.name: hero for hero in all_heroes}

