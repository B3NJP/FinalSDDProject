import re
import pygame

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
                        tempText = pygame.key.name(event.key)
                        if event.mod & (pygame.KMOD_SHIFT | pygame.KMOD_CAPS):
                            tempText = tempText.upper()
                        text += tempText
                if event.type == pygame.MOUSEBUTTONDOWN:
                    finished = True
        if re.fullmatch(pattern, text):
            break
    return text
    