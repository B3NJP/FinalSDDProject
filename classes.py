import math, copy
import functions
import pygame

class Map:
    def __init__(self):
        pass

class Character:
    def __init__(self, name, stats, loc=[0,0], script=None, alive=True, image=None):
        self.name = name
        self.HP = stats[0]
        self.MP = stats[1]
        self.ATK = stats[2]
        self.DEF = stats[3]
        self.INT = stats[4]
        self.RES = stats[5]
        self.DEX = stats[6]
        self.AGI = stats[7]
        self.loc = loc
        self.alive = alive
        self.script = script
        self.maxHP = stats[0]
        self.maxMP = stats[1]
        
        if image:
            self.image = pygame.transform.scale(pygame.image.load(image), [100, 100])
        else:
            self.image = None
        
    def run(self, map, player):
        if self.script:
            self.script(self, map, player)
            
    def artPoints(self):
        return math.floor(self.DEX*1.5 + self.AGI*0.75)

class Art:
    def __init__(self, name, mods, cc, mv, rg, cost, atkType = 'PHY'): #Note: cc - crowd control, mv - player movement, rg - range
        self.name = name
        self.mods = mods
        self.cc = cc
        self.mv = mv
        self.rg = rg
        self.cost = cost
        self.atkType = atkType

class Combo:
    def __init__(self, name, arts, dirs):
        self.name = name
        self.arts = arts
        self.count = len(arts)
        self.dirs = dirs
        
    def run(self, attacker, defenderList, rotation):
        if functions.compareCosts(attacker, self):
            cdirs = functions.rotate(copy.deepcopy(self.dirs), rotation)
            for i,v in enumerate(self.arts):
                functions.useArt(attacker, defenderList, v, i, cdirs[i])
            
    def cost(self):
        total = 0
        for i in self.arts:
            total += i.cost
        return total