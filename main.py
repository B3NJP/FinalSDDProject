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
dispPauseMenu = False

# Further Pause Menu
buttonSize = [600, 100]
resButton = pygame.Surface(buttonSize)
editComboButton = pygame.Surface(buttonSize)
quitButton = pygame.Surface(buttonSize)
menuFont = pygame.font.Font(None, 40)
def drawPauseMenuButtons(cursor):
    resButton.fill(white)
    pygame.draw.rect(resButton, black, [0, 0] + buttonSize, 10)
    resButton.blit(menuFont.render("Resume", True, black), [(buttonSize[0]-menuFont.size("Resume")[0])/2, (buttonSize[1]-menuFont.size("Resume")[1])/2])
    pauseMenu.blit(resButton, [200, 100])
    
    resButton.fill(white)
    pygame.draw.rect(resButton, black, [0, 0] + buttonSize, 10)
    resButton.blit(menuFont.render("Edit Combos", True, black), [(buttonSize[0]-menuFont.size("Edit Combos")[0])/2, (buttonSize[1]-menuFont.size("Resume")[1])/2])
    pauseMenu.blit(resButton, [200, 300])
    
    quitButton.fill(white)
    pygame.draw.rect(quitButton, black, [0, 0] + buttonSize, 10)
    quitButton.blit(menuFont.render("Quit", True, black), [(buttonSize[0]-menuFont.size("Quit")[0])/2, (buttonSize[1]-menuFont.size("Resume")[1])/2])
    pauseMenu.blit(quitButton, [200, 500])
    
# Combo Menu
dispComboMenu = False

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

while True:
    # Gets events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
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
            if event.key == pygame.K_ESCAPE and not dispComboMenu:
                dispPauseMenu = not dispPauseMenu
                
            # Checks if number (to select combo)
            if pygame.key.name(event.key) in "1234567890":
                chosenCombo = combos[(int(pygame.key.name(event.key))-1)%10] # The % 10 here is unnessasary, using index -1 gets last in array, but I would rather not rely on a lucky coincidence which makes the code unclear

        if event.type == pygame.MOUSEBUTTONDOWN: # Mouse buttons
            if event.button == 1:
                if dispPauseMenu:
                    if 200 <= event.pos[0] <= 800:
                        if 100 <= event.pos[1] <= 200:
                            dispPauseMenu = False
                            
                        if 300 <= event.pos[1] <= 400:
                            dispPauseMenu = False
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
        for i in range(0, min(10, len(combos))):
            col = black if combos[i] != chosenCombo else blue
            comboWindow.blit(font.render(str(i+1) + ": " + combos[i].name, True, col), [10, 10 + 15*i])
        screen.blit(comboWindow, [screenSize[0]-comboWindowSize[0], screenSize[1]-comboWindowSize[1]])
        
    if dispPauseMenu:
        pauseMenu.fill(greyMenu)
        drawPauseMenuButtons('test')
        screen.blit(pauseMenu, [0,0])
        
    if dispComboMenu:
        pass

    # Draws everything to screen
    pygame.display.flip()
