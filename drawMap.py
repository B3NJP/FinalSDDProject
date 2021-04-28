import pygame

box = [100, 100]
black = 0, 0, 0
white = 255, 255, 255

def draw(map, units, camera, screen):
    for i in range(0, len(map)):
        for j in range(0, len(map[i])):
            if ((i+camera[1])*100 < screen.get_height() and (i+camera[1])*100 > -100): # If the spot is within the selected area
                if ((j+camera[0])*100 < screen.get_width() and (j+camera[0])*100 > -100): # If the spot is within the selected area
                    pygame.draw.rect(screen, black, [(j+camera[0])*100, (i+camera[1])*100]+box, 1) # Draws map lines

    for i in units:
        if ((i.loc[1]+camera[1])*100 < screen.get_height() and (i.loc[1]+camera[1])*100 > -100): # If the spot is within the selected area
            if ((i.loc[0]+camera[0])*100 < screen.get_width() and (i.loc[0]+camera[0])*100 > -100): # If the spot is within the selected area
                pygame.draw.circle(screen, black, [(i.loc[0]+camera[0])*100+50, (i.loc[1]+camera[1])*100+50], 40, 1) # Draws map lines