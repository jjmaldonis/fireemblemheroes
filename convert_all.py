import json


def main():
    data = open("all.csv").readlines()

    data[0]
    data = [line.strip().split(",") for line in data]

    header = data[0]
    data = data[1:]

    for i, unit in enumerate(data):
        name = unit[0]
        unit = unit[1:]
        unit = [int(x) for x in unit]
        if unit[-1] == 1:
            unit[-1] = True
        else:
            unit[-1] = False
        if unit[0] == 1:
            unit[0] = "Infantry"
        elif unit[0] == 2:
            unit[0] = "Cavalry"
        elif unit[0] == 3:
            unit[0] = "Flying"
        elif unit[0] == 4:
            unit[0] = "Armored"
        if unit[1] == 0:
            unit[1] = "Colorless"
        if unit[1] == 1:
            unit[1] = "Red"
        if unit[1] == 2:
            unit[1] = "Green"
        if unit[1] == 3:
            unit[1] = "Blue"
        if unit[2] == 0:
            unit[2] = "Physical"
        if unit[2] == 1:
            unit[2] = "Dragon"
        if unit[2] == 2:
            unit[2] = "Magic"
        unit = [name] + unit
        data[i] = unit

    # ['Abel', 'Cavalry', 'Red', 'Physical', 44, 41, 27, 25, 25, 162, True]

    for unit in data:
        name = unit[0]
        unit_type = unit[1]
        color = unit[2]
        damage_type = unit[3]
        hp = unit[4]
        attack = unit[5]
        speed = unit[6]
        defense = unit[7]
        resistance = unit[8]
        brave_weapon = unit[9]
        skills = []

        unit = {
            "name": name,
            "unit_type": unit_type,
            "stats": {
                "hp": hp,
                "attack": attack,
                "speed": speed,
                "defense": defense,
                "resistance": resistance
            },
            "skills": [
            ],
            "weapon": "Unknown"
        }

        with open("data/{}.json".format(name.replace(" ", "_").lower()), "w") as f:
            f.write(json.dumps(unit, indent=4))


if __name__ == "__main__":
    main()
