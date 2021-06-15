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
    if dir == 'N':
        for i in mods:
            if i == 'F':
                loc[1] -= 1
            elif i == 'B':
                loc[1] += 1
            elif i == 'R':
                loc[0] += 1
            elif i == 'L':
                loc[0] -= 1
    if dir == 'S':
        for i in mods:
            if i == 'F':
                loc[1] += 1
            elif i == 'B':
                loc[1] -= 1
            elif i == 'R':
                loc[0] -= 1
            elif i == 'L':
                loc[0] += 1
    if dir == 'E':
        for i in mods:
            if i == 'F':
                loc[0] += 1
            elif i == 'B':
                loc[0] -= 1
            elif i == 'R':
                loc[1] += 1
            elif i == 'L':
                loc[1] -= 1
                
    if dir == 'W':
        for i in mods:
            if i == 'F':
                loc[0] -= 1
            elif i == 'B':
                loc[0] += 1
            elif i == 'R':
                loc[1] -= 1
            elif i == 'L':
                loc[1] += 1
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
    # print(ccLoc)
    for i in defenders:
        i.loc[0] += ccLoc[0]
        i.loc[1] += ccLoc[1]

    mvLoc = determineLoc(dir, art.mv)
    attacker.loc[0] += mvLoc[0]
    attacker.loc[1] += mvLoc[1]

def rotate(dirs, dir):
    convertfrom = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
    convertto = {0: 'N', 1: 'E', 2: 'S', 3: 'W'}
    count = convertfrom[dir]
    for i in range(0, len(dirs)):
        num = convertfrom[dirs[i]]
        num = (num+count)%4
        dirs[i] = convertto[num]
    print(dirs)
    return dirs
    
# def useCombo(attacker, defenderList, arts, dirs): Removed in place of having combo in combo class
#     for i,v in enumerate(arts):
#         useArt(attacker, defenderList, v, i, dirs[i])
