class Map:
    def __init__(self):
        pass

class Character:
    def __init__(self, name, stats):
        self.name = name
        self.HP = stats[0]
        self.MP = stats[1]
        self.ATK = stats[2]
        self.DEF = stats[3]
        self.INT = stats[4]
        self.RES = stats[5]
        self.DEX = stats[6]
        self.AGI = stats[7]
        self.loc = [0,0]

class Art:
    def __init__(self, name, mods, cc, mv, rg, cost): #Note: cc - crowd control, mv - player movement, rg - range
        self.name = name
        self.mods = mods
        self.cc = cc
        self.mv = mv
        self.rg = rg
        self.cost = cost
