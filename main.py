# Created by following tutorial at https://opensource.com/article/17/12/game-framework-python
# Additional resources at https://coderslegacy.com/python/python-pygame-tutorial/

import pygame
from pygame.locals import *
import sys
import os
import random

'''
Variables
'''
worldx = 800    # x dimension
worldy = 600    # y dimension
fps = 40        # framerate
ani = 4         # animation cycles

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (255, 255, 255)
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
        self.movex = 0  # move along x
        self.movey = 0  # move along y
        self.frame = 0  # count frames
        self.images = []

        for i in range(0,8):
            img = pygame.image.load(os.path.join('assets/supertux', f'walk-{i}.png')).convert()
            img.convert_alpha()     # optimize alpha
            img.set_colorkey(ALPHA) # set alpha
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
    
    def control(self, x, y):
        '''
        Control player movement
        '''
        self.movex += x
        self.movey += y
    
    def update(self):
        '''
        Update sprite position
        '''
        self.rect.x += self.movex
        self.rect.y += self.movey

        # Moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame//ani], True, False)
        
        # Moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.images[self.frame//ani]


class Bug(pygame.sprite.Sprite):
    '''
    Spawn a bug
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.images = []

        for i in range(0,6):
            img = pygame.image.load(os.path.join('assets/opp2_sprites', f'bug-{i}.png')).convert()
            img.convert_alpha()     # optimize alpha
            img.set_colorkey(ALPHA) # set alpha
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
    
    def move(self, x, y):
        self.movex += x
        self.movey += y
    
    def update(self):
        self.rect.x += self.movex
        self.rect.y += self.movey

        # Moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame//ani], True, False)
        
        # Moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.images[self.frame//ani]

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

bug = Bug()
bug.rect.x = random.randint(100,500)
bug.rect.y = 0
bug_list = pygame.sprite.Group()
bug_list.add(bug)

steps = 10  # how many pixels to move

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
        
        '''
        @TODO: 
        Allow movement through mouse click
        Reference documentation available at:
        https://www.pygame.org/docs/ref/mouse.html#module-pygame.mouse
        '''
        
        if event.type == KEYDOWN:       
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps,0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps,0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('jump')

        if event.type == KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps,0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps,0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('jump end')

            if event.key == ord('q'):
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False

    world.blit(backdrop, backdropbox)
    player.update()
    player_list.draw(world) # draw player
    bug.update()
    bug_list.draw(world)

    pygame.display.flip()
    clock.tick(fps)


