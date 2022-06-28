import pygame
import random
import math
from pygame import mixer

# initializing the pygame
pygame.init()

# creating the screen
screen = pygame.display.set_mode([800, 600])

# background
background = pygame.image.load('galexy.png')

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("space Battle")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('ship.png')
playerx = 380
playery = 480
playerx_change = 0

# Enemy
enemyImg = []
enemyx = []
enemyy = []
enemy_changex = []
enemy_changey = []
num_of_enemys = 6                       # number of enemys
for i in range(num_of_enemys):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(0, 150))
    enemy_changex.append(.5)
    enemy_changey.append(80)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bullet_changex = 0
bullet_changey = 20
bullet_state = 'ready'
#score
score_value = 0
font= pygame.font.Font('freesansbold.ttf',32)

textx=10
texty=10
#game over text

over_font= pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score = font.render("score  : "+str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER" ,True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    screen.fill((30, 144, 255))

    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystrok is pressed or not
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = - 1
            if event.key == pygame.K_RIGHT:
                playerx_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound= mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)

        # if the keystrok is relesed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # Adding boundery to the spaceship
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # adding boundery to the enemy
    #enemy movement
    for i in range(num_of_enemys):
        #game over

        if enemyy[i] > 420:
            for j in range(num_of_enemys):
                enemyy[j] = 2000
            game_over_text()
            break

        enemyx[i]+= enemy_changex[i]
        if enemyx[i] <= 0:
            enemy_changex[i] = 0.3
            enemyy[i] += enemy_changey[i]
        elif enemyx[i] >= 736:
            enemy_changex[i] = -0.3
            enemyy[i] += enemy_changey[i]

        # collision
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            explosion_sound = mixer.Sound('explo.wav')
            explosion_sound.play()
            bullety = 480
            bullet_state = 'ready'
            score_value += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i]= random.randint(50, 150)
        enemy(enemyx[i], enemyy[i],i)
    # bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletx, bullety)
        bullety -= bullet_changey



    # calling functions
    player(playerx, playery)
    show_score(textx,texty)
    pygame.display.update()
