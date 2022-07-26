from pip import main
import pygame 
import random
import time
from pygame import mixer

pygame.init()

#screen creating
screen=pygame.display.set_mode((800, 600)) 

#background 
background=pygame.image.load("spaceBackground.png")
mixer.Sound("background.wav").play(-1)

#title and icon
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load("icon.png"))

#player
playerImg= pygame.image.load("spaceship.png")
playerX=370
playerY=480
playerX_Change=0

#bullet
bulletImg= pygame.image.load("bullet.png")
bulletX=1000
bullets = [[bulletX,480,"ready"],[bulletX,480,"ready"],[bulletX,480,"ready"]]

#enemy
enemyImg= pygame.image.load("enemy.png")
enemyX=random.randint(0,736)
enemyY=random.randint(50,150)
enemyX_Change=0.3
enemyY_Change=32  

#score
score=0
font=pygame.font.Font("freesansbold.ttf", 32)
def show_score(x,y):
    screen.blit((font.render("Score: "+str(score),True,(255,255,255))),(x,y))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y):
    screen.blit(enemyImg,(x,y))

def fire_bullet(bullet:list):
    if bullet[2] == "fire":
        if bullet[0] == 1000:
            bullet[0] = playerX
        screen.blit(bulletImg,(bullet[0]+16,bullet[1]+10))

def isCollission(enemyX, enemyY, bulletX, bulletY):
    if abs(bulletX-enemyX)<=27 and abs(bulletY-enemyY)<=27:
        return True
    else:
        return False

#Game loop
    #to open game window
running= True
while running:
    screen.blit(background,(0,0))
    for event in pygame.event.get(): 
        if event.type== pygame.QUIT:
            running=False 
        #controlling keystroke 
        if event.type==pygame.KEYDOWN:
            if event.key== pygame.K_LEFT:
                playerX_Change=-0.6
            if event.key== pygame.K_RIGHT:
                playerX_Change=0.6
            if event.key== pygame.K_SPACE:
                for bullet in bullets:
                    if bullet[2]=="ready":
                        bullet[2] = "fire"
                        mixer.Sound("laser.wav").play()
                        bullet[1]-=0.6+score*0.031
                        fire_bullet(bullet)
                        break   
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key== pygame.K_RIGHT:
                playerX_Change=0

    #player movement
    playerX+=playerX_Change
    if playerX <=0:
        playerX=0
    elif playerX>=736:
        playerX=736  

    #enemy movement
    enemyX+=enemyX_Change
    if enemyX>=736:
        enemyX_Change=-0.3+score*-0.03
        enemyY+=enemyY_Change
    if enemyX<=0:
        enemyX_Change=abs(enemyX_Change)
        enemyY+=enemyY_Change

    #bullet movement
    for bullet in bullets:
        if bullet[1]<=0:
            bullet[1]=480
            bullet[2]="ready"
            bullet[0]=1000
        if bullet[2] == "fire":
            fire_bullet(bullet)
            bullet[1]-=0.6

    #collision
    for bullet in bullets:
        collission=isCollission(enemyX, enemyY, bullet[0], bullet[1])
        if collission:
            mixer.Sound("explosion.wav").play()
            enemyX=random.randint(0,736)
            enemyY=random.randint(50,150) 
            score+=1
            bullet[1]=480
            bullet[2]="ready"
            bullet[0]=1000   

    #game over
    def game_over(x,y):
        over=(pygame.font.Font("freesansbold.ttf", 64)).render("GAME OVER!",True,(255,255,255))
        screen.blit(over,(x,y))
    if enemyY>=440:
        game_over(200,250)
        mixer.Sound("gameOver.wav").play()
        enemyY=1000
        enemyY_Change, enemyX_Change, playerX_Change= 0,0,0
        bullets = [[bulletX,480,"fire"],[bulletX,480,"fire"],[bulletX,480,"fire"]]

    show_score(10,10)
    player(playerX,playerY)
    enemy(enemyX,enemyY)
    pygame.display.update()