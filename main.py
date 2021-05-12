import math, random, sys
import pygame
import classes, functions, exampleArts, drawMap
pygame.init()

# Basic Values
box = [100, 100]
screenSize = [1000, 800]
black = 0, 0, 0
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


# Arts Window
artsWindowSize = [300, 400]
artsWindow = pygame.Surface(statWindowSize)
page = 0
artsWindow.set_alpha(200)
dispArtsWind = False


# Text Font
font = pygame.font.Font(None, 25)

# Temporary
Alice = classes.Character('Alice', [28, 27, 9, 7, 11, 6, 8, 9])
Bill = classes.Character('Bill', [27, 20, 13, 6, 6, 6, 9, 8])

Alice.loc = [1,3]
Bill.loc = [6,6]
units = [Alice, Bill]

cArt = exampleArts.pierce

testComboA = [exampleArts.pierce, exampleArts.greatPierce]
testDirsA = ['N', 'N']
testComboB = [exampleArts.broadSlash]*8
testDirsB = ['N', 'E', 'E', 'S', 'S', 'W', 'W', 'N']

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

            if event.key == pygame.K_u:
                functions.useArt(Alice, units, cArt, 0, 'N')
            if event.key == pygame.K_h:
                functions.useArt(Alice, units, cArt, 0, 'W')
            if event.key == pygame.K_j:
                functions.useArt(Alice, units, cArt, 0, 'S')
            if event.key == pygame.K_k:
                functions.useArt(Alice, units, cArt, 0, 'E')

            if event.key == pygame.K_z:
                functions.combo(Alice, units, testComboA, testDirsA)
            if event.key == pygame.K_x:
                functions.combo(Alice, units, testComboB, testDirsB)

            if event.key == pygame.K_m:
                dispStatWind = not dispStatWind
            if event.key == pygame.K_n:
                dispArtWind = not dispArtWind

        if event.type == pygame.MOUSEBUTTONDOWN: # Mouse buttons
            if event.button == 1:
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

    # Draws everything to screen
    pygame.display.flip()
