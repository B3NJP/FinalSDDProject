import math, random
import classes, ai

def getRandom(n): #gets random int 0 <= num < n
    return math.floor(random.random()*n)

def randomRange(n, m):
    return math.floor(n+random.random()*(m-n+1))

# Remember 8 stats HP MP ATK DEF INT RES DEX AGI
class bandit(classes.Character):
    def __init__(self):
        name = "Bandit" # Consider making name generator later
        stats = [
        25+getRandom(3),
        15+getRandom(3),
        20+getRandom(3),
        18+getRandom(3),
        10+getRandom(3),
        12+getRandom(3),
        17+getRandom(3),
        15+getRandom(3),
        ]
        sc = ai.warrior
        img = "Assets/Enemies/png/Bandit.png"
        super().__init__(name, stats, script=sc, image=img)