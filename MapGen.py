import random, math

def makeRoom():
    w = math.floor(random.random()*4)+2
    h = math.floor(random.random()*4)+2
    return [w,h]
    
def makeHall(wide):
    if wide:
        w = math.floor(random.random()*5)+5
        h = 2#math.floor(random.random()*2)+2
    else:
        w = 2#math.floor(random.random()*2)+2
        h = math.floor(random.random()*5)+5
    return [w,h]

class Room:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
def genMap(size):
    # current = [makeRoom()]
    rooms = []
    cloks = [[0,0]]
    cSize = 0
    while cloks and cSize < size:
        c = makeRoom()#current.pop(0)
        loc = cloks.pop(0)
        croom = Room(loc[0], loc[1], c[0], c[1])
        rooms += [croom]
        # hall1 = makeHall(True)
        # rooms += [Room(croom.x-hall1[0], croom.y+2, hall1[0], hall1[1]]
        tallhall = makeHall(False)
        rooms += [Room(croom.x+2, croom.y+croom.h, tallhall[0], tallhall[1])]
        cloks += [[croom.x, croom.y+croom.h+tallhall[1]]]
        widehall = makeHall(True)
        rooms += [Room(croom.x+croom.w, croom.y+2, widehall[0], widehall[1])]
        cloks += [[croom.x+croom.w+widehall[0], croom.y]]
        cSize += 1
    return rooms
    
def drawMap(rooms):
    fullMap = [[1]*30 for i in range(0, 30)]
    # print([i.h for i in rooms])
    for i in rooms:
        for j in range(0, i.h):
            fullMap[i.y+j][i.x:i.x+i.w] = [0]*i.w
    return fullMap
    
def printMap(map):
    for i in map:
        print(''.join([str(j) for j in i]))
        
printMap(drawMap(genMap(3)))
        