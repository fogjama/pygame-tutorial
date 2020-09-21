import pygame
from pygame.locals import *
import sys
import os

'''
Variables
'''
worldx = 800    # x dimension
worldy = 600    # y dimension
fps = 40        # framerate
ani = 4         # animation cycles

main = True

'''
Objects
'''



'''
Setup

'''
clock = pygame.time.Clock()
pygame.init()

world = pygame.display.set_mode([worldx,worldy])
backdrop = pygame.image.load(os.path.join('assets/kenny/Backgrounds','backgroundColorDesert.png'))
backdropbox = world.get_rect()

'''
Main Loop
'''

while main == True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False
        
        if event.type == KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False

    world.blit(backdrop, backdropbox)

    pygame.display.flip()
    clock.tick(fps)


