import math, random, sys
import pygame
import classes, functions, exampleArts, drawMap
pygame.init()

# Basic Values
box = [100, 100]
screenSize = [1000, 800]
black = 0, 0, 0
blue = 0, 0, 255
white = 255, 255, 255

screen = pygame.display.set_mode(screenSize)

grid = [['0']*8]*8

camera = [0,0]

selected = None


# Stat Window
statWindowSize = [300, 400]
statWindow = pygame.Surface(statWindowSize)
statWindow.set_alpha(200)
dispStatWind = False


# Combo Window
comboWindowSize = [300, 400]
comboWindow = pygame.Surface(comboWindowSize)
page = 0
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

def drawButton(surface, text, font, location, size, backgroundCol, textCol):
    button = pygame.Surface(size)
    button.fill(backgroundCol)
    pygame.draw.rect(button, black, [0, 0] + size, 10)
    button.blit(font.render(text, True, textCol), [(size[0]-font.size(text)[0])/2, (size[1]-font.size(text)[1])/2])
    surface.blit(button, location)
    return button

def drawPauseMenuButtons(cursor):
    drawButton(pauseMenu, "Resume", menuFont, [200, 100], buttonSize, white, black)
    drawButton(pauseMenu, "Edit Combos", menuFont, [200, 300], buttonSize, white, black)
    drawButton(pauseMenu, "Quit", menuFont, [200, 500], buttonSize, white, black)
    
# Combo Menu
dispComboMenu = False
comboMenuSize = [700, 600]
comboMenuLoc = [150, 100]
comboMenu = pygame.Surface(comboMenuSize)
arrowFont = pygame.font.Font(None, 60)
def drawComboMenu(highlight):
    comboMenu.fill(white)
    pygame.draw.rect(comboMenu, black, [0, 0] + comboMenuSize, 10)
    
    # Initial Rectangle Boxes
    pygame.draw.rect(comboMenu, black, [0, 0, 200, 600], 10)
    pygame.draw.rect(comboMenu, black, [200, 0, 200, 600], 10)
    pygame.draw.rect(comboMenu, black, [400, 0, 200, 600], 10)
    
    # New Button
    drawButton(comboMenu, "New Combo", menuFont, [0, 500], [200, 100], white, black)
    
    # Arrow Page Buttons
    drawButton(comboMenu, "<", arrowFont, [200, 500], [100, 100], white, black)
    drawButton(comboMenu, ">", arrowFont, [300, 500], [100, 100], white, black)
    
    # Delete Button
    drawButton(comboMenu, "Delete", menuFont, [400, 500], [200, 100], white, black)
    
    # List Combos - For both of these, consider using buttons instead of numbers
    comboMenu.blit(menuFont.render("Combos:", True, black), [(200-menuFont.size("Combos:")[0])/2, (100-menuFont.size("Combos:")[1])/2])
    for i in range(0, len(combos)):
        # text = str(i+1) + ": " + combos[i].name
        # comboMenu.blit(menuFont.render(text, True, black), [20, 100+i*40])
        if combos[i] == highlight:
            drawButton(comboMenu, combos[i].name, menuFont, [0, 100+i*50], [200, 50], white, blue)
        else:
            drawButton(comboMenu, combos[i].name, menuFont, [0, 100+i*50], [200, 50], white, black)
        
    # List Known Arts
    comboMenu.blit(menuFont.render("Arts:", True, black), [(200-menuFont.size("Arts:")[0])/2+200, (100-menuFont.size("Arts:")[1])/2])
    for i in range(0, min(len(knownArts),10)):
        # text = str((i+1)%10) + ": " + knownArts[i].name # Make adjustment for longer art names
        # comboMenu.blit(menuFont.render(text, True, black), [220, 100+i*40])
        drawButton(comboMenu, knownArts[i].name, menuFont, [200, 100+i*50], [200, 50], white, black)
        
    # Shows the selected combo
    if highlight:
        comboMenu.blit(menuFont.render(highlight.name, True, black), [(200-menuFont.size(highlight.name)[0])/2+400, (100-menuFont.size(highlight.name)[1])/2])
        for i in range(0, len(highlight.arts)):
            drawButton(comboMenu, highlight.arts[i].name, menuFont, [400, 100+i*50], [200, 50], white, black)
            drawButton(comboMenu, highlight.dirs[i], menuFont, [600, 100+i*50], [100, 50], white, black)
            
        

# Text Font
font = pygame.font.Font(None, 25)

# Temporary
Alice = classes.Character('Alice', [28, 27, 9, 7, 11, 6, 8, 9])
Bill = classes.Character('Bill', [27, 20, 13, 6, 6, 6, 9, 8])

Alice.loc = [1,3]
Bill.loc = [6,6]
units = [Alice, Bill]

cArt = exampleArts.pierce

testDirsA = ['N', 'N']
testComboA = classes.Combo('Test1', [exampleArts.pierce, exampleArts.greatPierce], testDirsA)

testDirsB = ['N', 'E', 'E', 'S', 'S', 'W', 'W', 'N']
testComboB = classes.Combo('Test2', [exampleArts.broadSlash]*8, testDirsB)

combos = [testComboA, testComboB]
chosenCombo = None
menuSelectedCombo = None#testComboA

knownArts = [exampleArts.pierce, exampleArts.broadSlash, exampleArts.greatPierce]

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
                if event.key == pygame.K_UP:
                    camera[1] += .5
                if event.key == pygame.K_RIGHT:
                    camera[0] -= .5
                if event.key == pygame.K_DOWN:
                    camera[1] -= .5
                if event.key == pygame.K_LEFT:
                    camera[0] += .5

                if event.key == pygame.K_w:
                    Alice.loc[1] -= 1
                if event.key == pygame.K_a:
                    Alice.loc[0] -= 1
                if event.key == pygame.K_s:
                    Alice.loc[1] += 1
                if event.key == pygame.K_d:
                    Alice.loc[0] += 1

                if event.key == pygame.K_p:
                    cArt = exampleArts.pierce
                if event.key == pygame.K_g:
                    cArt = exampleArts.greatPierce
                if event.key == pygame.K_b:
                    cArt = exampleArts.broadSlash

                # if event.key == pygame.K_u:
                #     functions.useArt(Alice, units, cArt, 0, 'U')
                # if event.key == pygame.K_h:
                #     functions.useArt(Alice, units, cArt, 0, 'L')
                # if event.key == pygame.K_j:
                #     functions.useArt(Alice, units, cArt, 0, 'D')
                # if event.key == pygame.K_k:
                #     functions.useArt(Alice, units, cArt, 0, 'R')
                if chosenCombo:
                    if event.key == pygame.K_u:
                        chosenCombo.run(Alice, units, 'N')
                    if event.key == pygame.K_k:
                        chosenCombo.run(Alice, units, 'E')
                    if event.key == pygame.K_j:
                        chosenCombo.run(Alice, units, 'S')
                    if event.key == pygame.K_h:
                        chosenCombo.run(Alice, units, 'W')

                # if event.key == pygame.K_z:
                #     testComboA.run(Alice, units, testDirsA)
                # if event.key == pygame.K_x:
                #     testComboB.run(Alice, units, testDirsB)

                if event.key == pygame.K_m:
                    dispStatWind = not dispStatWind
                if event.key == pygame.K_n:
                    dispComboWind = not dispComboWind
                    
                # Checks if number (to select combo)
                if pygame.key.name(event.key) in "1234567890":
                    chosenCombo = combos[(int(pygame.key.name(event.key))-1)]

        if event.type == pygame.MOUSEBUTTONDOWN: # Mouse buttons
            if event.button == 1:
                if dispPauseMenu:
                    if dispComboMenu:
                        if comboMenuLoc[0] <= event.pos[0] <= comboMenuLoc[0]+comboMenuSize[0]:
                            if comboMenuLoc[0] <= event.pos[0] <= comboMenuLoc[0]+200 and comboMenuLoc[1]+100 <= event.pos[1] <= comboMenuLoc[1] + comboMenuSize[1] - 100:
                                if 0 <= math.floor((event.pos[1] - comboMenuLoc[1]-100)/50) < len(combos):
                                    menuSelectedCombo = combos[math.floor((event.pos[1] - comboMenuLoc[1]-100)/50)]
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
    
    drawMap.draw(grid, units, camera, screen)

    if dispStatWind and selected:
        statWindow.fill(white)
        pygame.draw.rect(statWindow, black, [0, 0] + statWindowSize, 10)
        statWindow.blit(font.render(selected.name, True, black), [10, 10])
        statWindow.blit(font.render('HP: ' + str(selected.HP), True, black), [10, 25])
        statWindow.blit(font.render('MP: ' + str(selected.MP), True, black), [10, 40])
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
