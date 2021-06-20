import math, random

# dimensions = 50,50
# tempMap = [['X']*50 for i in range(0, 50)]

def doRooms(countRange, sizeRanges, dimensions):
    rooms = []
    for i in range(0, countRange[0]+math.floor((countRange[1]-countRange[0])*random.random())):
        loc = [math.floor(random.random()*(dimensions[0]-sizeRanges[0][1])), math.floor(random.random()*(dimensions[1]-sizeRanges[1][1]))]
        size = [sizeRanges[0][0]+math.floor(random.random()*(sizeRanges[0][1]-sizeRanges[0][0])), sizeRanges[1][0]+math.floor(random.random()*(sizeRanges[1][1]-sizeRanges[1][0]))]
        addto = True
        for j in rooms:
            if interfere(loc+size, j):
                addto = False
                break
        if addto:
            rooms += [loc+size]
    return rooms
    
def interfere(r1, r2):
    if r2[0] < r1[0] < r2[0]+r2[2]:
            if r2[1] < r1[1] < r2[1]+r2[3]:
                return True
    if r1[0] < r2[0] < r1[0]+r1[2]:
            if r1[1] < r2[1] < r1[1]+r1[3]:
                return True
    return False

def drawRooms(rooms, arr):
    for i in rooms:
        for j in range(i[1], i[1]+i[3]):
            for k in range(i[0], i[0]+i[2]):
                arr[j][k] = '0'

def connectRooms(room1, room2):
    # vertical = True#random.random()>0.5
    locs = []
    # if vertical:
    x = math.floor(random.random()*room1[2]) + room1[0]
    y = room1[1]
    down = False
    if room1[1] < room2[1]:
        y += room1[3]-1
        down = True
    if not down:
        finalY = min(room2[1]+math.floor(random.random()*room2[3]),room1[1])
        while y > finalY:
            y -= 1
            locs += [[x, y]]
    if down:
        finalY = max(room2[1]+math.floor(random.random()*room2[3]),room1[1]+room1[3])
        while y < finalY:
            y += 1
            locs += [[x, y]]
    left = False
    if x > room2[0]:
        left = True
    if left:
        finalX = min(room2[0]+math.floor(random.random()*room2[2]), x)
        while x > finalX:
            x -= 1
            locs += [[x, y]]
    if not left:
        finalX = max(room2[0]+math.floor(random.random()*room2[2]), x)
        while x < finalX:
            x += 1
            locs += [[x, y]]
    return locs
# rooms = doRooms([5, 10], [[7,10],[7,10]], dimensions)
# drawRooms(rooms, tempMap)
# #connect1 = connectRooms(rooms[0], rooms[1])
# connects = [connectRooms(rooms[i], rooms[i+1]) for i in range(0,len(rooms)-1)]
# for i in connects:
#     for j in i:
#         tempMap[j[1]][j[0]] = '0'
# for i in tempMap:
#     print(''.join(i))