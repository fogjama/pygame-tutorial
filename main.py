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
fps = 20        # framerate
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

    def __init__(self, x, y, p_img):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0  # move along x
        self.movey = 0  # move along y
        self.frame = 0  # count frames
        self.health = 10 # track player health
        self.images = []

        for i in range(0,8):
            img = pygame.image.load(os.path.join('assets/supertux', f'{p_img}-{i}.png')).convert()
            img.convert_alpha()     # optimize alpha
            img.set_colorkey(ALPHA) # set alpha
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def control(self, x, y):
        '''
        Control player movement
        '''
        self.movex += x
        self.movey += y
    
    def update(self):
        
        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            self.health -= 1
            print(self.health)

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


class Enemy(pygame.sprite.Sprite):
    '''
    Spawn a bug
    '''
    def __init__(self, x, y, img_file):
        pygame.sprite.Sprite.__init__(self)
        # self.movex = 0
        # self.movey = 0
        self.frame = 0
        self.images = []

        for i in range(0,6):
            img = pygame.image.load(os.path.join('assets/opp2_sprites', f'{img_file}-{i}.png')).convert()
            img.convert_alpha()     # optimize alpha
            img.set_colorkey(ALPHA) # set alpha
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0
    
    def move(self, distance, speed):
        # self.movex += x
        # self.movey += y

        # distance = 60
        # speed = 3

        if self.counter >= 0 and self.counter <= distance:
            self.rect.x += speed
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.images[self.frame//ani]
        elif self.counter >= distance and self.counter <= distance*2: 
            self.rect.x -= speed
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame//ani], True, False)
        else:
            self.counter = 0

        self.counter += 1


class Level():
    def bad(lvl, eloc):
        if lvl == 1:
            enemy = Enemy(eloc[0],eloc[1],'bug')
            enemy_list = pygame.sprite.Group()
            enemy_list.add(enemy)
        if lvl == 2:
            bug = Enemy(eloc[0], eloc[1], 'bug')
            bug2 = Enemy(eloc[2], eloc[3], 'bug')
            enemy_list = pygame.sprite.Group()
            enemy_list.add(bug)
            enemy_list.add(bug2)

        return enemy_list
    
    def ground(lvl,x,y,w,h, img_file):
        ground_list = pygame.sprite.Group()

        ground = Platform(x, y, w, h, img_file)
        ground_list.add(ground)
        
        return ground_list
    
    def ground_tile(lvl,gloc,tx,ty,img_file):
        ground_list = pygame.sprite.Group()

        i=0
        while i < len(gloc):
            ground = Platform(gloc[i], worldy-ty, tx, ty, img_file)
            ground_list.add(ground)
            i += 1
        
        return ground_list
    
    def platform(lvl):
        plat_list = pygame.sprite.Group()

        if lvl == 1:
            plat = Platform(200, worldy-150-100, 96, 32, 'supertux/forestlog.png')
            plat_list.add(plat)
            plat = Platform(500, worldy-150-200, 96, 32, 'supertux/forestlog.png')
            plat_list.add(plat)
        if lvl == 2:
            plat = Platform(230, worldy-150-100, 128, 32, 'supertux/foresttiles-1a.png')
            plat_list.add(plat)
            plat = Platform(330, worldy-150-200, 128, 32, 'supertux/foresttiles-1a.png')
            plat_list.add(plat)
            plat = Platform(430, worldy-150-300, 128, 32, 'supertux/foresttiles-1a.png')
            plat_list.add(plat)
        
        return plat_list

class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, imgw, imgh, img_file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('assets/',img_file)).convert()
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = xloc
        self.rect.y = yloc

'''
Setup

'''
clock = pygame.time.Clock()
pygame.init()

world = pygame.display.set_mode([worldx,worldy])
backdrop = pygame.image.load(os.path.join('assets/kenny/Backgrounds','backgroundColorDesert.png'))
backdropbox = world.get_rect()

gloc = []
tx = 128
ty = 150

i = 0
while i <= (worldx/tx)+tx:
    gloc.append(i*tx)
    i += 1

player = Player(0,worldy-ty-27,'walk')   # Spawn player
# player.rect.x = 0   # Go to x
# player.rect.y = 0   # Go to y
player_list = pygame.sprite.Group()
player_list.add(player)

eloc = []
eloc = [random.randint(100,200),0,random.randint(250,350),0]
lvl = 2
enemy_list = Level.bad(lvl, eloc)

ground_list = Level.ground_tile(lvl, gloc, tx, ty, 'supertux/foresttiles-1.png')
plat_list = Level.platform(2)

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
            if event.key == K_LEFT or event.key == ord('a'):
                player.control(-steps,0)
            if event.key == K_RIGHT or event.key == ord('d'):
                player.control(steps,0)
            if event.key == K_UP or event.key == ord('w') or event.key == K_SPACE:
                print('jump')

        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == ord('a'):
                player.control(steps,0)
            if event.key == K_RIGHT or event.key == ord('d'):
                player.control(-steps,0)
            if event.key == K_UP or event.key == ord('w') or event.key == K_SPACE:
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
    enemy_list.draw(world) # draw enemies
    ground_list.draw(world)
    plat_list.draw(world)
    for e in enemy_list:
        e.move(60, random.randint(2,6))

    pygame.display.flip()
    clock.tick(fps)


