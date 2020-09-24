# Created by following tutorial at https://opensource.com/article/17/12/game-framework-python
# Additional resources at https://coderslegacy.com/python/python-pygame-tutorial/

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

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

main = True

'''
Objects
'''

class Player(pygame.sprite.Sprite):
    '''
    Spawn a player
    '''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        for i in range(0,8):
            img = pygame.image.load(os.path.join('assets/supertux', f'walk-{i}.png')).convert()
            img.convert_alpha()     # optimize alpha
            img.set_colorkey(ALPHA) # set alpha
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

'''
Setup

'''
clock = pygame.time.Clock()
pygame.init()

world = pygame.display.set_mode([worldx,worldy])
backdrop = pygame.image.load(os.path.join('assets/kenny/Backgrounds','backgroundColorDesert.png'))
backdropbox = world.get_rect()

player = Player()   # Spawn player
player.rect.x = 0   # Go to x
player.rect.y = 0   # Go to y
player_list = pygame.sprite.Group()
player_list.add(player)

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
    player_list.draw(world) # draw player

    pygame.display.flip()
    clock.tick(fps)


