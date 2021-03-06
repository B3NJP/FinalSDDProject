import math, random, sys, copy, time
import pygame
import classes, functions, exampleArts, drawMap, pygameFunctions, ai, MapGen2, exampleEnemies
pygame.init()

# Basic Values
box = [100, 100]
screenSize = [1000, 800]
black = 0, 0, 0
blue = 0, 0, 255
red = 255, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(screenSize)

# Prepares map
dimensions = (30,30)
grid = [['X']*dimensions[0] for i in range(0, dimensions[1])]
rooms = MapGen2.doRooms([5, 10], [[5,8],[5,8]], dimensions)
MapGen2.drawRooms(rooms, grid)
connects = [MapGen2.connectRooms(rooms[i], rooms[i+1]) for i in range(0,len(rooms)-1)]
for i in connects:
    for j in i:
        grid[j[1]][j[0]] = '0'

# Starting Location:
def getFreeLocation(grid):
    loc = [math.floor(random.random()*dimensions[0]), math.floor(random.random()*dimensions[1])]
    while grid[loc[1]][loc[0]] == 'X':
        loc = [math.floor(random.random()*dimensions[0]), math.floor(random.random()*dimensions[1])]
    return loc

startLoc = getFreeLocation(grid)

camera = [5-startLoc[0],4-startLoc[1]]

# selected = None


# Stat Window
statWindowSize = [300, 400]
statWindow = pygame.Surface(statWindowSize)
statWindow.set_alpha(200)
dispStatWind = False


# Combo Window
comboWindowSize = [300, 400]
comboWindow = pygame.Surface(comboWindowSize)
comboWindow.set_alpha(200)
dispComboWind = False

# Pause Menu
greyMenu = 100, 100, 100, 150
pauseMenu = pygame.Surface(screenSize)
pauseMenu.fill(greyMenu)
dispPauseMenu = False

# Further Pause Menu
buttonSize = [600, 100]
menuFont = pygame.font.Font(None, 40)

def drawPauseMenuButtons(cursor):
    pygameFunctions.drawButton(pauseMenu, "Resume", menuFont, [200, 100], buttonSize, white, black)
    pygameFunctions.drawButton(pauseMenu, "Edit Combos", menuFont, [200, 300], buttonSize, white, black)
    pygameFunctions.drawButton(pauseMenu, "Quit", menuFont, [200, 500], buttonSize, white, black)
    
# Combo Menu
dispComboMenu = False
comboMenuSize = [700, 600]
comboMenuLoc = [150, 100]
comboMenu = pygame.Surface(comboMenuSize)
arrowFont = pygame.font.Font(None, 60)
artPage = 0
def drawComboMenu(highlight):
    comboMenu.fill(white)
    pygame.draw.rect(comboMenu, black, [0, 0] + comboMenuSize, 10)
    
    # Initial Rectangle Boxes
    pygame.draw.rect(comboMenu, black, [0, 0, 200, 600], 10)
    pygame.draw.rect(comboMenu, black, [200, 0, 200, 600], 10)
    pygame.draw.rect(comboMenu, black, [400, 0, 200, 600], 10)
    
    # New Button
    pygameFunctions.drawButton(comboMenu, "New Combo", menuFont, [0, 500], [200, 100], white, black)
    
    # Arrow Page Buttons
    pygameFunctions.drawButton(comboMenu, "<", arrowFont, [200, 500], [100, 100], white, black)
    pygameFunctions.drawButton(comboMenu, ">", arrowFont, [300, 500], [100, 100], white, black)
    
    # Delete Button
    pygameFunctions.drawButton(comboMenu, "Delete", menuFont, [400, 500], [200, 100], white, black)
    
    # List Combos - For both of these, consider using buttons instead of numbers
    comboMenu.blit(menuFont.render("Combos:", True, black), [(200-menuFont.size("Combos:")[0])/2, (100-menuFont.size("Combos:")[1])/2])
    for i in range(0, len(combos)):
        # text = str(i+1) + ": " + combos[i].name
        # comboMenu.blit(menuFont.render(text, True, black), [20, 100+i*40])
        if combos[i] == highlight:
            pygameFunctions.drawButton(comboMenu, combos[i].name, menuFont, [0, 100+i*50], [200, 50], white, blue)
        else:
            pygameFunctions.drawButton(comboMenu, combos[i].name, menuFont, [0, 100+i*50], [200, 50], white, black)
        
    # List Known Arts
    comboMenu.blit(menuFont.render("Arts:", True, black), [(200-menuFont.size("Arts:")[0])/2+200, (100-menuFont.size("Arts:")[1])/2])
    for i in range(0, len(knownArts[artPage*8:artPage*8+8])):
        # text = str((i+1)%10) + ": " + knownArts[i].name # Make adjustment for longer art names
        # comboMenu.blit(menuFont.render(text, True, black), [220, 100+i*40])
        pygameFunctions.drawButton(comboMenu, knownArts[i+artPage*8].name, menuFont, [200, 100+i*50], [200, 50], white, black)
        
    # Shows the selected combo
    if highlight:
        comboMenu.blit(menuFont.render(highlight.name, True, black), [(200-menuFont.size(highlight.name)[0])/2+400, (100-menuFont.size(highlight.name)[1])/2])
        pygameFunctions.drawButton(comboMenu, str(highlight.cost()) + "/" + str(player.artPoints()), menuFont, [600, 0], [100, 100], white, black if (player.artPoints() >= highlight.cost()) else red)
        for i in range(0, len(highlight.arts)):
            pygameFunctions.drawButton(comboMenu, highlight.arts[i].name, menuFont, [400, 100+i*50], [200, 50], white, black)
            pygameFunctions.drawButton(comboMenu, highlight.dirs[i], menuFont, [600, 100+i*50], [100, 50], white, black)


# Text Font
font = pygame.font.Font(None, 25)

# Temporary -- Also (self, name, stats, loc=[0,0], script=None, alive=True, image=None) -- HP, MP, ATK, DEF, INT, RES, DEX, AGI
player = classes.Character('Player', [28, 27, 20, 17, 19, 16, 22, 17], loc=startLoc, image="Assets/Enemies/png/Fighter.png")
selected = player
# Bill = classes.Character('Bill', [27, 20, 13, 6, 6, 6, 9, 8], loc=getFreeLocation(grid), script=ai.warrior, image="Assets/Enemies/png/Bandit.png")

# player.loc = [1,3]
# Bill.loc = [6,6]
units = [player]#[player, Bill]
# enemies = [Bill]

# Make Enemies
def makeEnemy(eType, grid):
    c = eType()
    c.loc = getFreeLocation(grid)
    return c

enemies = [makeEnemy(exampleEnemies.bandit, grid) for i in range(0, 5)]
units += enemies

# testDirsA = ['N', 'N']
# testComboA = classes.Combo('Test1', [exampleArts.pierce, exampleArts.greatPierce], testDirsA)
# 
# testDirsB = ['N', 'E', 'E', 'S', 'S', 'W', 'W', 'N']
# testComboB = classes.Combo('Test2', [exampleArts.broadSlash]*8, testDirsB)

# combos = [testComboA, testComboB]
chosenCombo = None
menuSelectedCombo = None#testComboA

# knownArts = [exampleArts.pierce, exampleArts.broadSlash, exampleArts.greatPierce]
# knownArts = exampleArts.allArts

# Changed initial arts
knownArts = [exampleArts.pierce, exampleArts.broadSlash]
unknownArts = copy.copy(exampleArts.allArts)
for i in knownArts:
    unknownArts.remove(i)
random.shuffle(unknownArts)
knownArts.sort(key=lambda n: n.name)

pierceSlash = classes.Combo("Pierce Slash", [exampleArts.pierce, exampleArts.broadSlash], ['N', 'N'])
combos = [pierceSlash]

# Enemy turns
endTurn = False

def newLevel():
    # Prepares variables
    global grid, player, camera, enemies, units
    
    # Prepares Map
    grid = [['X']*dimensions[0] for i in range(0, dimensions[1])]
    rooms = MapGen2.doRooms([5, 10], [[5,8],[5,8]], dimensions)
    MapGen2.drawRooms(rooms, grid)
    connects = [MapGen2.connectRooms(rooms[i], rooms[i+1]) for i in range(0,len(rooms)-1)]
    for i in connects:
        for j in i:
            grid[j[1]][j[0]] = '0'
        
    # Prepares Player    
    player.HP = player.maxHP
    player.loc = getFreeLocation(grid)

    camera = [5-player.loc[0],4-player.loc[1]]
    
    # Prepares Enemies
    enemies = [makeEnemy(exampleEnemies.bandit, grid) for i in range(0, 5)]
    units = [player] + enemies
    
def restart():
    global knownArts, unknownArts
    knownArts = [exampleArts.pierce, exampleArts.broadSlash]
    unknownArts = copy.copy(exampleArts.allArts)
    for i in knownArts:
        unknownArts.remove(i)
    random.shuffle(unknownArts)
    knownArts.sort(key=lambda n: n.name)
    newLevel()

pygameFunctions.openingMenu(screenSize, screen)

# Developer Console
def console():
    global knownArts, unknownArts
    command = input()
    if command == 'art':
        knownArts += unknownArts
        unknownArts = []
    knownArts.sort(key=lambda n: n.name) # Consider making a learn arts function
        
while True:
    # Gets events
    for event in pygame.event.get(): # Note consider moving these into functions in another file
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if dispComboMenu:
                    dispComboMenu = False   
                dispPauseMenu = not dispPauseMenu
                
            if not dispPauseMenu:
                # Camera Scroll
                if event.key == pygame.K_UP:
                    camera[1] += .5
                if event.key == pygame.K_RIGHT:
                    camera[0] -= .5
                if event.key == pygame.K_DOWN:
                    camera[1] -= .5
                if event.key == pygame.K_LEFT:
                    camera[0] += .5
                
                # Developer Console
                if event.key == pygame.K_c:
                    console()
                
                # Player Movement
                if event.key == pygame.K_w:
                    if player.loc[1] > 0:
                        if grid[player.loc[1]-1][player.loc[0]] == '0':
                            player.loc[1] -= 1
                            endTurn = True
                if event.key == pygame.K_a:
                    if player.loc[0] > 0:
                        if grid[player.loc[1]][player.loc[0]-1] == '0':
                            player.loc[0] -= 1
                            endTurn = True
                if event.key == pygame.K_s:
                    if player.loc[1] < len(grid)-1:
                        if grid[player.loc[1]+1][player.loc[0]] == '0':
                            player.loc[1] += 1
                            endTurn = True
                if event.key == pygame.K_d:
                    if player.loc[0] < len(grid[player.loc[1]])-1:
                        if grid[player.loc[1]][player.loc[0]+1] == '0':
                            player.loc[0] += 1
                            endTurn = True

                # if event.key == pygame.K_p:
                #     cArt = exampleArts.pierce
                # if event.key == pygame.K_g:
                #     cArt = exampleArts.greatPierce
                # if event.key == pygame.K_b:
                #     cArt = exampleArts.broadSlash

                # if event.key == pygame.K_u:
                #     functions.useArt(player, units, cArt, 0, 'U')
                # if event.key == pygame.K_h:
                #     functions.useArt(player, units, cArt, 0, 'L')
                # if event.key == pygame.K_j:
                #     functions.useArt(player, units, cArt, 0, 'D')
                # if event.key == pygame.K_k:
                #     functions.useArt(player, units, cArt, 0, 'R')
                if chosenCombo:
                    if event.key == pygame.K_u:
                        chosenCombo.run(player, enemies, 'N')
                        endTurn = True
                    if event.key == pygame.K_k:
                        chosenCombo.run(player, enemies, 'E')
                        endTurn = True
                    if event.key == pygame.K_j:
                        chosenCombo.run(player, enemies, 'S')
                        endTurn = True
                    if event.key == pygame.K_h:
                        chosenCombo.run(player, enemies, 'W')
                        endTurn = True

                # if event.key == pygame.K_z:
                #     testComboA.run(player, units, testDirsA)
                # if event.key == pygame.K_x:
                #     testComboB.run(player, units, testDirsB)

                if event.key == pygame.K_m:
                    dispStatWind = not dispStatWind
                if event.key == pygame.K_n:
                    dispComboWind = not dispComboWind
                    
                # Checks if number (to select combo)
                if pygame.key.name(event.key) in "123456789":
                    if int(pygame.key.name(event.key)) <= len(combos):
                        chosenCombo = combos[(int(pygame.key.name(event.key))-1)]

        if event.type == pygame.MOUSEBUTTONDOWN: # Mouse buttons
            if event.button == 1:
                if dispPauseMenu:
                    if dispComboMenu:
                        if comboMenuLoc[0] <= event.pos[0] <= comboMenuLoc[0]+comboMenuSize[0] and comboMenuLoc[1] <= event.pos[1] <= comboMenuLoc[1]+comboMenuSize[1]:
                            if comboMenuLoc[0] <= event.pos[0] <= comboMenuLoc[0]+200:
                                # Select Combo
                                if comboMenuLoc[1]+100 <= event.pos[1] <= comboMenuLoc[1] + comboMenuSize[1] - 100:
                                    if 0 <= math.floor((event.pos[1] - comboMenuLoc[1]-100)/50) < len(combos):
                                        menuSelectedCombo = combos[math.floor((event.pos[1] - comboMenuLoc[1]-100)/50)]
                                        
                                # New Combo
                                if comboMenuLoc[1]+comboMenuSize[1]-100 <= event.pos[1] <= comboMenuLoc[1]+comboMenuSize[1]:
                                    if len(combos) < 10:
                                        tempName = pygameFunctions.textInput(pattern = '((\w)| )+')
                                        combos += [classes.Combo(tempName, [], [])]
                            
                            # Changes Art Page
                            if comboMenuLoc[0]+200 <= event.pos[0] <= comboMenuLoc[0]+400 and comboMenuLoc[1]+comboMenuSize[1]-100 <= event.pos[1] <= comboMenuLoc[1]+comboMenuSize[1]:
                                if comboMenuLoc[0]+200 <= event.pos[0] <= comboMenuLoc[0]+300 and len(knownArts) > 8:
                                    artPage -= 1
                                    artPage %= math.ceil(len(knownArts)/8)
                                elif comboMenuLoc[0]+300 <= event.pos[0] <= comboMenuLoc[0]+400 and len(knownArts) > 8:
                                    artPage += 1
                                    artPage %= math.ceil(len(knownArts)/8)
                                    
                            if menuSelectedCombo:
                                # Add Art
                                if comboMenuLoc[0]+200 <= event.pos[0] <= comboMenuLoc[0]+400:
                                    if comboMenuLoc[1]+100 <= event.pos[1] <= comboMenuLoc[1] + comboMenuSize[1] - 100:
                                        if 0 <= math.floor((event.pos[1] - comboMenuLoc[1]-100)/50) < len(knownArts[artPage*8:artPage*8+8]):
                                            menuSelectedCombo.arts += [knownArts[artPage*8 + math.floor((event.pos[1] - comboMenuLoc[1]-100)/50)]]
                                            menuSelectedCombo.dirs += ['N']
                                        
                                if comboMenuLoc[0]+400 <= event.pos[0] <= comboMenuLoc[0]+600: 
                                    # Rename Combo
                                    if comboMenuLoc[1] <= event.pos[1] <= comboMenuLoc[1]+100:
                                        tempName = pygameFunctions.textInput(pattern = '((\w)| )+')
                                        menuSelectedCombo.name = tempName
                                        
                                    # Remove Art
                                    if comboMenuLoc[1]+100 <= event.pos[1] <= comboMenuLoc[1] + comboMenuSize[1] - 100:
                                        if 0 <= math.floor((event.pos[1] - comboMenuLoc[1]-100)/50) < len(menuSelectedCombo.arts):
                                            menuSelectedCombo.arts.pop(math.floor((event.pos[1] - comboMenuLoc[1]-100)/50))
                                            menuSelectedCombo.dirs.pop(math.floor((event.pos[1] - comboMenuLoc[1]-100)/50))
                                            
                                    # Delete Combo
                                    if comboMenuLoc[1]+comboMenuSize[1]-100 <= event.pos[1] <= comboMenuLoc[1]+comboMenuSize[1]:
                                        combos.remove(menuSelectedCombo)
                                        menuSelectedCombo = None
                                        
                                # Change Art Direction
                                if comboMenuLoc[0]+600 <= event.pos[0] <= comboMenuLoc[0]+700 and comboMenuLoc[1]+100 <= event.pos[1] <= comboMenuLoc[1] + comboMenuSize[1] - 100:
                                    if 0 <= math.floor((event.pos[1] - comboMenuLoc[1]-100)/50) < len(menuSelectedCombo.dirs):
                                        menuSelectedCombo.dirs[math.floor((event.pos[1] - comboMenuLoc[1]-100)/50)] = functions.rotate([copy.deepcopy(menuSelectedCombo.dirs)[math.floor((event.pos[1] - comboMenuLoc[1]-100)/50)]], 'E')[0]
                    else:
                        if 200 <= event.pos[0] <= 800:
                            if 100 <= event.pos[1] <= 200:
                                dispPauseMenu = False
                                
                            if 300 <= event.pos[1] <= 400:
                                dispComboMenu = True
                                
                            if 500 <= event.pos[1] <= 600:
                                sys.exit()
                else:
                    # Gets location of mouse (adjusted for scroll)
                    location = [int((event.pos[0]-camera[0]*100)//100), int((event.pos[1]-camera[1]*100)//100)]

                    for i in units:
                        if i.loc == location:
                            selected = i
                            break
                        
                        
    screen.fill(white) # Makes the screen white
    # screen.fill(black) # Makes the screen black
    
    drawMap.draw(grid, units, camera, screen)
    
    if endTurn:
        pygame.display.flip()
        time.sleep(0.2)
        endTurn = False
        toRemove = []
        for i in enemies:
            # Kills enemies outside of space
            if i.loc[0] < 0 or i.loc[0] >= len(grid[i.loc[1]]) or i.loc[1] < 0 or i.loc[1] >= len(grid):
                i.HP = 0
            elif grid[i.loc[1]][i.loc[0]] == 'X':
                i.HP = 0
            
            # If it has HP run else die
            if i.HP > 0:
                i.run(grid, player)
            else:
                i.alive = False
                if selected == i:
                    selected = player
                if unknownArts:
                    if random.random() > 0.5: # 50% Chance of aquiring a new art
                        knownArts += [unknownArts.pop()]
                        knownArts.sort(key=lambda n: n.name)
                toRemove += [i]
        for i in toRemove:
            units.remove(i)
            enemies.remove(i)
        if player.loc[0] < 0 or player.loc[0] >= len(grid[player.loc[1]]) or player.loc[1] < 0 or player.loc[1] >= len(grid):
            player.HP = 0
        elif grid[player.loc[1]][player.loc[0]] == 'X':
            player.HP = 0
        if player.HP <= 0:
            restart()
        if len(enemies) == 0:
            newLevel()

    if dispStatWind and selected:
        statWindow.fill(white)
        pygame.draw.rect(statWindow, black, [0, 0] + statWindowSize, 10)
        statWindow.blit(font.render(selected.name, True, black), [10, 10])
        statWindow.blit(font.render('HP: ' + str(selected.HP) + '/' + str(selected.maxHP), True, black), [10, 25])
        statWindow.blit(font.render('MP: ' + str(selected.MP) + '/' + str(selected.maxMP), True, black), [10, 40])
        statWindow.blit(font.render('ATK: ' + str(selected.ATK), True, black), [10, 55])
        statWindow.blit(font.render('DEF: ' + str(selected.DEF), True, black), [10, 70])
        statWindow.blit(font.render('INT: ' + str(selected.INT), True, black), [10, 85])
        statWindow.blit(font.render('RES: ' + str(selected.RES), True, black), [10, 100])
        statWindow.blit(font.render('DEX: ' + str(selected.DEX), True, black), [10, 115])
        statWindow.blit(font.render('AGI: ' + str(selected.AGI), True, black), [10, 130])
        screen.blit(statWindow, [0, screenSize[1]-statWindowSize[1]])
        
    if dispComboWind:
        comboWindow.fill(white)
        pygame.draw.rect(comboWindow, black, [0, 0] + comboWindowSize, 10)
        for i in range(0, min(9, len(combos))):
            col = black if combos[i] != chosenCombo else blue
            comboWindow.blit(font.render(str(i+1) + ": " + combos[i].name, True, col), [10, 10 + 15*i])
        screen.blit(comboWindow, [screenSize[0]-comboWindowSize[0], screenSize[1]-comboWindowSize[1]])
        
    if dispPauseMenu:
        pauseMenu.fill(greyMenu)
        if dispComboMenu:
            drawComboMenu(menuSelectedCombo)
            pauseMenu.blit(comboMenu, comboMenuLoc)
        else:
            drawPauseMenuButtons('test')
        screen.blit(pauseMenu, [0,0])
        
    

    # Draws everything to screen
    pygame.display.flip()
