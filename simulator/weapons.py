import copy
import enum
import json


class DamageType(enum.Enum):
    MAGIC = "Magic"
    PHYSICAL = "Physical"


class WeaponColor(enum.Enum):
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    COLORLESS = "Colorless"


class Special(object):
    """An abstract base class for special weapon abilities."""
    # Not fully implemented because I'm not sure of the details yet
    def __init__(self, name, stat_modifiers):
        """
        name : str
        stat_modifiers : Stats
        """
        self.name = name
        self.stat_modifiers = stat_modifiers

    def conditional(self, game_state):
        """Returns True if the special should be active given this game state, else False."""
        raise NotImplemented

    def bind_to_hero(self, hero):
        self.hero = hero


class AddTotalBonusesToDamageDealt(Special):
    def __init__(self, name):
        super().__init__(name, None)

    @property
    def bonus_damage(self):
        return sum(buff.hp for buff in self.hero.permanent_buffs + self.hero.buffs_this_combat if buff.hp > 0) + \
               sum(buff.attack for buff in self.hero.permanent_buffs + self.hero.buffs_this_combat if buff.attack > 0) + \
               sum(buff.speed for buff in self.hero.permanent_buffs + self.hero.buffs_this_combat if buff.speed > 0) + \
               sum(buff.defense for buff in self.hero.permanent_buffs + self.hero.buffs_this_combat if buff.defense > 0) + \
               sum(buff.resistance for buff in self.hero.permanent_buffs + self.hero.buffs_this_combat if buff.resistance > 0)




class Weapon(object):
    def __init__(self, name, color, damage_type, range_, special=None):
        """
        color : Enum<WeaponColor>
        damage_type : Enum<DamageType>
        range : int (1 or 2)
        special : Special  # Not sure how handle do this yet
        """
        self.name = name
        self.color = color
        self.damage_type = damage_type
        self.range = range_
        self.special = special
        self.hero = None

    @classmethod
    def from_json(cls, data=None, filename=None):
        if filename is not None:
            data = json.load(open(filename))
        else:
            assert data is not None
        raise NotImplemented  # I don't know if we will even have json data for weapons or what format it will be in

    def bind_to_hero(self, hero):
        self.hero = hero
        if self.special:
            self.special.bind_to_hero(hero)

    #def __eq__(self, other):
    #    return self.color == other.color
    def __lt__(self, other):
        return (self.color == WeaponColor.RED and other.color == WeaponColor.BLUE) or \
               (self.color == WeaponColor.BLUE and other.color == WeaponColor.GREEN) or \
               (self.color == WeaponColor.GREEN and other.color == WeaponColor.RED)
    def __gt__(self, other):
        return (other.color == WeaponColor.RED and self.color == WeaponColor.BLUE) or \
               (other.color == WeaponColor.BLUE and self.color == WeaponColor.GREEN) or \
               (other.color == WeaponColor.GREEN and self.color == WeaponColor.RED)

Gronnblade = Weapon(
    name = "Gronnblade",
    color = WeaponColor("Green"),
    damage_type = DamageType("Magic"),
    range_ = 2,
    special = AddTotalBonusesToDamageDealt("Gronnblade")
)

Falchion = Weapon(
    name = "Falchion",
    color = WeaponColor("Red"),
    damage_type = DamageType("Physical"),
    range_ = 1,
    special = None # TODO
)

BlarravenPlus = Weapon(
    name = "Blarraven+",
    color = WeaponColor.BLUE,
    damage_type = DamageType.MAGIC,
    range_ = 2,
    special = None # TODO
)

FujinYumi = Weapon(
    name = "Fujin Yumi",
    color = WeaponColor.COLORLESS,
    damage_type = DamageType.PHYSICAL,
    range_ = 2,
    special = None # TODO
)

Unknown = Weapon(
    name = "Unknown",
    color = WeaponColor.COLORLESS,
    damage_type = DamageType.PHYSICAL,
    range_ = 1,
    special = None
)


all_weapons = {weapon.name: copy.copy(weapon) for weapon in [Gronnblade, Falchion, BlarravenPlus, FujinYumi, Unknown]}

