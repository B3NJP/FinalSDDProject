import re
import pygame

def textInput(pattern = '.*'):
    while True: # Repeat until not re.match(pattern, text)
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
                    else:
                        text += pygame.key.name(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    finished = True
        if not re.match(pattern, text):
            break
    return text
    