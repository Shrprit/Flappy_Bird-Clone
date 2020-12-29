import random # for generating random no
import sys #sys.exit to exit the program
import pygame
from pygame.locals import *

# Global variable
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallry/sprites/bird.png'
BACKGROUND = 'gallry/sprites/backgrond_images.png'
PIPE = 'gallry/sprites/pipe.png'

def welcomeScreen():
    #shows welcome image on screen
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

                #if the user presses space or up key, start game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
               # SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
    #create two pipes to blit on screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    # my list of upper pipe
    upperPipes = [
        {'x':SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},

    ]
    # my list of lower pipe
    lowerPipes = [
        {'x':SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},

    ]

    pipeVelocityX = -4
    playerVelocityY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.type == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelocityY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            return
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidpos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidpos <= playerMidPos < pipeMidpos + 4:
                score+=1
                print(f"your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelocityY <playerMaxVelY and not playerFlapped:
            playerVelocityY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelocityY , GROUNDY - playery - playerHeight)

        #moves pipe to the left
        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVelocityX
            lowerPipe['x'] += pipeVelocityX

        # add a new pipe  when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])


        # if the pipe is out of screen then remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))


        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset , SCREENHEIGHT*0.12))
            xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery > GROUNDY - 25 or playery < 0 :
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x'] ) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if(playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    return False



def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x':pipeX, 'y': -y1}, #upper pipe
        {'x':pipeX, 'y': y2} #lower pipe
    ]
    return pipe

if __name__ == "__main__":
    pygame.init() 
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Shruti')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallry/sprites/0.png').convert_alpha(),
        pygame.image.load('gallry/sprites/1.png').convert_alpha(),
        pygame.image.load('gallry/sprites/2.png').convert_alpha(),
        pygame.image.load('gallry/sprites/3.png').convert_alpha(),
        pygame.image.load('gallry/sprites/4.png').convert_alpha(),
        pygame.image.load('gallry/sprites/5.png').convert_alpha(),
        pygame.image.load('gallry/sprites/6.png').convert_alpha(),
        pygame.image.load('gallry/sprites/7.png').convert_alpha(),
        pygame.image.load('gallry/sprites/8.png').convert_alpha(),
        pygame.image.load('gallry/sprites/9.png').convert_alpha(),
    )
    GAME_SPRITES['message'] = pygame.image.load('gallry/sprites/start.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallry/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
    )

    #game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallry/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallry/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallry/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallry/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallry/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() #shows welcome screen to user until he presses a button
        mainGame() #this is the main game function





     
