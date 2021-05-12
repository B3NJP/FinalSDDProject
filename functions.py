import math, random, copy, time

def damageCalculation(attacker, defender, modifiers, atkType, comboLevel):
    finalMods = {'HP':1,'MP':1,'ATK':1,'DEF':1,'INT':1,'RES':1,'DEX':1,'AGI':1,'DMG':1}
    for i in modifiers:
        finalMods[i[0]] *= i[1]
    damage = 0

    if atkType == "PHY":
        damage += attacker.ATK*finalMods['ATK'] - defender.DEF*finalMods['DEF']
    elif atkType == "MAG":
        damage += attacker.INT*finalMods['INT'] - defender.RES*finalMods['RES']

    if comboLevel == 0:
        if random.random()>((attacker.DEX*finalMods['DEX'] - defender.AGI*finalMods['AGI'])*0.04 + 0.5):
            print((attacker.DEX*finalMods['DEX'] - defender.AGI*finalMods['AGI'])*0.04 + 0.5)
            print("Miss")
            return 0

    damage *= finalMods['DMG']
    damage *= 1 + comboLevel/10
    if damage < 0:
        damage = 0
    print("Damage: " + str(damage))
    return damage

def dealBasicDamage(attacker, defender, modifiers, atkType, comboLevel):
    damage = damageCalculation(attacker, defender, modifiers, atkType, comboLevel)
    defender.HP -= damage

def findDefenders(defenders, locs):
    defens = []
    for i in defenders:
        if i.loc in locs:
            defens += [i]
    return defens

def determineLoc(dir, mods):
    loc = [0,0]
    angle = {'N': 0, 'E': math.pi/2, 'S': math.pi, 'W': math.pi*3/2}
    if i == 'F': #Note to future self: still unfinished, need to fix the sin and cos
        loc[0] += math.sin(angle[dir])
        loc[1] -= math.cos(angle[dir])
    elif i == 'B':
        loc[0] -= math.sin(angle[dir])
        loc[1] += math.cos(angle[dir])
    elif i == 'R':
        loc[0] += math.sin(angle[dir])
        loc[1] += math.sin(angle[dir])
    elif i == 'L':
        loc[0] += math.sin(angle[dir])
        loc[1] += math.sin(angle[dir])
    if dir == 'U':
        for i in mods:
            if i == 'F':
                loc[1] -= 1
            elif i == 'B':
                loc[1] += 1
            elif i == 'R':
                loc[0] += 1
            elif i == 'L':
                loc[0] -= 1
    if dir == 'D':
        for i in mods:
            if i == 'F':
                loc[1] += 1
            elif i == 'B':
                loc[1] -= 1
            elif i == 'R':
                loc[0] -= 1
            elif i == 'L':
                loc[0] += 1
    if dir == 'L':
        for i in mods:
            if i == 'F':
                loc[0] -= 1
            elif i == 'B':
                loc[0] += 1
            elif i == 'R':
                loc[1] -= 1
            elif i == 'L':
                loc[1] += 1
    if dir == 'R':
        for i in mods:
            if i == 'F':
                loc[0] += 1
            elif i == 'B':
                loc[0] -= 1
            elif i == 'R':
                loc[1] += 1
            elif i == 'L':
                loc[1] -= 1
    return loc

def useArt(attacker, defenderList, art, combo, dir):
    locs = []
    for i in art.rg:
        loc = copy.deepcopy(attacker.loc)
        moddedLoc = determineLoc(dir, i)
        loc[0] += moddedLoc[0]
        loc[1] += moddedLoc[1]
        locs += [loc]

    defenders = findDefenders(defenderList, locs)
    for i in defenders:
        dmg = damageCalculation(attacker, i, art.mods, 'PHY', combo)
        i.HP -= dmg

    ccLoc = determineLoc(dir, art.cc)
    print(ccLoc)
    for i in defenders:
        i.loc[0] += ccLoc[0]
        i.loc[1] += ccLoc[1]

    mvLoc = determineLoc(dir, art.mv)
    attacker.loc[0] += mvLoc[0]
    attacker.loc[1] += mvLoc[1]

def combo(attacker, defenderList, arts, dirs):
    for i,v in enumerate(arts):
        useArt(attacker, defenderList, v, i, dirs[i])
