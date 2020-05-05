# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 21:56:46 2020

@author: mario
"""

import pygame
import random
import math


# initialise the environment
pygame.init()

# create screen, pixels
screen = pygame.display.set_mode((800,600))

background = pygame.image.load("space.jpg").convert()

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('start-button.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370 # put it at the bottom middle
playerY = 480
playerX_change = 0
playerY_change = 0


explosion = pygame.image.load('explosion.png')

life = 5
score = 0
game_over = False
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
lifeX =600
lifeY =10
killed = 0

def show_score(x,y):
    score_ = font.render("Score : " + str(score),True, (0,255,0))
    screen.blit(score_, (x,y))

def show_life(x=lifeX,y=lifeY):
    life_ = font.render("Life : " + str(life),True, (255,255,255))
    screen.blit(life_, (x,y))

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 11
# speed changes according to the enemies killed (increases difficulty)
enemy_speed = min(score//(killed+1) + 1,10) 

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(enemy_speed)
    enemyY_change.append(40)


#Bullet
# 'ready'= we don't see the bullet
# 'fire' =  bullet is moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

def player(x,y):
    screen.blit(playerImg,(x,y)) # draw
    
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y)) # draw

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg,(x+16,y+10)) # for the bullet to appear on the center
    
def isCollision(item1x,item1y,item2x,item2y):
    distance = math.sqrt((item1x-item2x)**2 + (item1y-item2y)**2)
    if distance <=27 :
        return True

def show_explosion(x,y):
    screen.blit(explosion,(x,y))
    pygame.time.wait(10)
    
# Game loop, infinite
running = True
while running:
    
    # give RGB background color
    screen.fill((0,0,0)) #black
    # background
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # if keystroke is pressed, check whether it is right or left
        if event.type== pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_UP:
                playerY_change = -1
            if event.key == pygame.K_DOWN:
                playerY_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX,bulletY)
        
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: 
                playerX_change = 0
    
    
    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0:
        playerX = 0
    # spaceship is 64x64 pixels
    if playerX >= 736:
        playerX = 736
        
    if playerY <= 300:
        playerY = 300
        playerY_change = 0
    if playerY >= 480:
        playerY = 480
        playerY_change = 0
    
    
    for i in range((killed//10 + 1)):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change[i]
        # spaceship is 64x64 pixels
        elif enemyX[i] >= 736:
            enemyX_change[i] = - enemy_speed
            enemyY[i] += enemyY_change[i]
        if enemyY[i] > 500:
            score -=1
        
        if isCollision(enemyX[i],enemyY[i],bulletX,bulletY):
            bulletY = playerY
            bulletX = playerX
            bullet_state = "ready"
            show_explosion(enemyX[i],enemyY[i])
            score += 1
            killed += 1
            enemyX[i] = random.randint(0,736) 
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i],i)
        
    
    # Bullet movement (we put it in the while loop to persist)
    # if the bullet goes out of the screen, we can fire another one
    if bulletY <=0 :
        bulletY = playerY
        bullet_state = 'ready'
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    
    
    for i in range(len(enemyX)):
        if isCollision(enemyX[i],enemyY[i],playerX,playerY):
            life -= 1
            show_explosion(enemyX[i],enemyY[i])
            enemyX[i] = random.randint(0,736) 
            enemyY[i] = random.randint(50,150)
            
    show_score(textX,textY)
    show_life()
    
    if life<=0:
        game_over = True
    
    if game_over:
        print(score)
        break
    player(playerX,playerY) # it needs to be on top of the screen
    pygame.display.update() # to show the updates
    
    
