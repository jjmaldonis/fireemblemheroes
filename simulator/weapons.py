import enum
import json


class DamageType(enum.Enum):
    MAGIC = "Magic"
    PHYSICAL = "Physical"


class WeaponColor(enum.Enum):
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"


class Special(object):
    """An abstract base class for special abilities."""
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

    @classmethod
    def from_json(cls, data=None, filename=None):
        if filename is not None:
            data = json.load(open(filename))
        else:
            assert data is not None
        raise NotImplemented  # I don't know if we will even have json data for weapons or what format it will be in

    def __eq__(self, other):
        return self.color == other.color
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
    special = None  # TODO
)

Falchion = Weapon(
    name = "Falchion",
    color = WeaponColor("Red"),
    damage_type = DamageType("Physical"),
    range_ = 1,
    special = None # TODO
)


all_weapons = {weapon.name: weapon for weapon in [Gronnblade, Falchion]}

