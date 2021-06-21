import sys, re
import pygame

black = 0, 0, 0
blue = 0, 0, 255
white = 255, 255, 255

def textInput(pattern = '.*'):
    while True: # Repeat until re.match(pattern, text)
        finished = False
        text = ""
        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key == pygame.K_RETURN:
                        finished = True
                    elif event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                        pass
                    else:
                        if event.key == pygame.K_SPACE:
                            tempText = ' '
                        else:
                            tempText = pygame.key.name(event.key)
                        if event.mod & (pygame.KMOD_SHIFT | pygame.KMOD_CAPS):
                            tempText = tempText.upper()
                        text += tempText
                if event.type == pygame.MOUSEBUTTONDOWN:
                    finished = True
        if re.fullmatch(pattern, text):
            break
    return text
    
def drawButton(surface, text, font, location, size, backgroundCol, textCol):
    button = pygame.Surface(size)
    button.fill(backgroundCol)
    pygame.draw.rect(button, black, [0, 0] + size, 10)
    button.blit(font.render(text, True, textCol), [(size[0]-font.size(text)[0])/2, (size[1]-font.size(text)[1])/2])
    surface.blit(button, location)
    return button

def openingMenu(screenSize, screenSurface):
    openMenu = pygame.Surface(screenSize)
    started = False
    buttonSize = [600, 100]
    menuFont = pygame.font.Font(None, 40)
    while not started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 200 <= event.pos[0] <= 800:
                        if 300 <= event.pos[1] <= 400:
                            started = True
                        if 500 <= event.pos[1] <= 600:
                            sys.exit()
                
        openMenu.fill(white)
        drawButton(openMenu, "New Game", menuFont, [200, 300], buttonSize, white, black)
        drawButton(openMenu, "Quit", menuFont, [200, 500], buttonSize, white, black)
        screenSurface.blit(openMenu, [0,0])
        pygame.display.flip()