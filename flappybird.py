import pygame 
import random
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)
WIDTH=289
HEIGHT=511
gameWindow= pygame.display.set_mode((WIDTH,HEIGHT) )
GROUNDY = HEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'bird.png'
BACKGROUND = 'background.png'
PIPE = 'pipe.png'
fps=60
def gameloop():
    exitgame=False
    gameover=False
    GAME_SPRITES['numbers'] = (
        pygame.image.load('0.png').convert_alpha(),
        pygame.image.load('1.png').convert_alpha(),
        pygame.image.load('2.png').convert_alpha(),
        pygame.image.load('3.png').convert_alpha(),
        pygame.image.load('4.png').convert_alpha(),
        pygame.image.load('5.png').convert_alpha(),
        pygame.image.load('6.png').convert_alpha(),
        pygame.image.load('7.png').convert_alpha(),
        pygame.image.load('8.png').convert_alpha(),
        pygame.image.load('9.png').convert_alpha(),
    )
    GAME_SPRITES['base'] =pygame.image.load('base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SOUNDS['die'] = pygame.mixer.Sound('die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('wing.wav')
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    score = 0
    playerx = int(WIDTH/5)
    playery = int(WIDTH/2)
    basex = 0
    newPipe1 = randompipe()
    newPipe2 = randompipe()
    upperPipes = [
        {'x': WIDTH+200, 'y':newPipe1[0]['y']},
        {'x': WIDTH+200+(WIDTH/2), 'y':newPipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': WIDTH+200, 'y':newPipe1[1]['y']},
        {'x': WIDTH+200+(WIDTH/2), 'y':newPipe2[1]['y']},
    ]
    goimg=pygame.image.load("game_over.jpg")
    goimg=pygame.transform.scale(goimg,(WIDTH,HEIGHT)).convert_alpha()
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccv = -8 
    playerFlapped = False
    clock=pygame.time.Clock()
    if (not os.path.exists("Highscore.txt")):
        with open("Highscore.txt",'w') as g:
            g.write("0")
    with open("Highscore.txt",'r') as f:
            highscore=f.read()
    while not exitgame:
        if gameover:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exitgame=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        # pygame.mixer.music.load("bg.mp3")
                        # pygame.mixer.music.play(-1)
                        pygame.mixer.music.pause()
                        gameloop()
            with open("Highscore.txt",'w') as f:
                f.write(str(highscore))
            gameWindow.blit(goimg,(0,0))
            show("Score:"+str(score),white,100,320)
            show("High Score:"+str(highscore),white,70,360)
        else:    
            for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        exitgame=True
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP):
                        if playery > 0:
                            playerVelY = playerFlapAccv
                            playerFlapped = True
                            GAME_SOUNDS['wing'].play()
            playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
                if pipeMidPos<= playerMidPos < pipeMidPos +4:
                    score +=1
                    if score>int(highscore):
                        highscore=score
                    # print(f"Your score is {score}")
                    GAME_SOUNDS['point'].play()
            if playerVelY <playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY
            if playerFlapped:
                playerFlapped = False
            playerHeight = GAME_SPRITES['player'].get_height()
            playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)
            for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX
            if 0<upperPipes[0]['x']<5:
                newpipe = randompipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])
            if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)
            gameWindow.blit(GAME_SPRITES['background'], (0, 0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                gameWindow.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                gameWindow.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

            gameWindow.blit(GAME_SPRITES['base'], (basex, GROUNDY))
            gameWindow.blit(GAME_SPRITES['player'], (playerx, playery))
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += GAME_SPRITES['numbers'][digit].get_width()
            Xoffset = (WIDTH - width)/2

            for digit in myDigits:
                gameWindow.blit(GAME_SPRITES['numbers'][digit], (Xoffset, HEIGHT*0.12))
                Xoffset += GAME_SPRITES['numbers'][digit].get_width()
            crashTest = iscollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
            if crashTest:
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()
                gameover=True
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()   
def welcome():
    exitgame=False
    while not exitgame:
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exitgame=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        # pygame.mixer.music.load("bg.mp3")
                        # pygame.mixer.music.play(-1)
                        gameloop()
        bgimg=pygame.image.load("cartoon_city.jpg")
        bgimg=pygame.transform.scale(bgimg,(WIDTH,HEIGHT)).convert_alpha()
        pygame.display.set_caption("Flappy Bird by Kushal Sharma")
        gameWindow.blit(bgimg,(0,0))
        show("Welcome to",white,75,80)
        show("Flappy Bird Game",white,40,120)
        show("Developed By",white,60,200)
        show("Kushal Sharma",white,48,240)
        show("Press enter to continue",white,5,300)
        pygame.display.update()
def randompipe():
    pipeheight=GAME_SPRITES['pipe'][0].get_height()
    offset=HEIGHT/2.6
    y2=offset+random.randint(0,int(HEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex=WIDTH+10
    y1=pipeheight-y2+offset
    pipe=[
        {'x':pipex,'y':-y1},
        {'x':pipex,'y':y2}
    ]
    return pipe
def iscollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False
def show(text,color,x,y):
    show_score=font.render(text,True,color)
    gameWindow.blit(show_score,[x,y])
if __name__ == "__main__":
    pygame.mixer.init()
    pygame.init()
    gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))
    font=pygame.font.SysFont(None,35)
    welcome()
    