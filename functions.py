from classes import *
from constants import *
import random

xm = xmargin                        # giving shorthand notations to the variables 
ym = ymargin
bh = boardHeight
bw = boardWidth
gbl= gapBetweenLadders
lw = ladderWidth


ladders=[                                                                   
             Ladder( (xm+550, bh-ym), (xm+550, bh-ym-gbl) ),
             Ladder( (xm+250, bh-ym-gbl-lw), (xm+250, bh-ym-2*gbl-lw)),
             Ladder( (xm+420, bh-ym-gbl-lw), (420+xm, bh-ym-gbl-30)),
             Ladder( (xm+420, bh-ym-gbl-55-lw),(xm+420, bh-ym-2*gbl-lw)),
             Ladder( (370+xm, bh-ym-2*gbl-2*lw),(370+xm, bh-ym-2*gbl-lw -30)),
             Ladder( (370+xm, bh-ym-2*gbl-2*lw-55), (370+xm, bh-ym-3*gbl-2*lw)),
             Ladder( (530+xm, bh-ym-2*gbl-2*lw), (530+xm,bh-ym-3*gbl-2*lw)) ,
             Ladder( (290+xm, bh-ym-3*gbl-3*lw),(290+xm, bh-ym-4*gbl-3*lw)),
             Ladder( (220+xm, bh-ym-4*gbl-4*lw),(220+xm, bh-ym-4*gbl-3*lw-30)),
             Ladder( (220+xm, bh-ym-4*gbl-4*lw-55),(220+xm,bh-ym-5*gbl-4*lw)),
             Ladder( (500+xm, bh-ym-4*gbl-4*lw), (500+xm, bh-ym -5*gbl- 4*lw)),
             Ladder( (300+xm,bh-ym-5*gbl-5*lw),(300+xm,bh-ym-6*gbl-5*lw))
        ]                         #list of all the ladders used in game


platforms= [
            Platform(xm, bh-ym, bw-2*xm, lw),
            Platform(xm,bh- ym- gbl- lw, 600, lw), 
            Platform(xm+200, bh- ym- 2*gbl- 2*lw, bw-2*xm-200,lw),
            Platform(xm , bh- ym- 3*gbl- 3*lw, 700, lw),
            Platform(xm+150 , bh- ym- 4*gbl - 4*lw, bw-2*xm-150, lw),
            Platform(xm, bh- ym-5*gbl- 5*lw, 610, lw),
            Platform(xm+100, ym+50, 300, lw)
            ]                   #list of all the platforms used in game

#Controls all the main game content

def startGameAnimation():
    pygame.init()
    global mySurf,fpsClock, player
    mySurf= Board(boardHeight, boardWidth, bgColor, xmargin, xmargin, ymargin , ymargin)
    fpsClock= pygame.time.Clock()
    welcome()
    player= Player(xmargin+5, boardHeight-ymargin-20, 20 ,10)
    donkey= Donkey(xmargin+5, ymargin+gapBetweenLadders+30, 30, 20)
    queen= Donkey(xmargin+200, ymargin + 50 -10 , 10, 10)

    set_display(mySurf, player, donkey, queen)

    for i in range(20):
        x= random.randint(0,len(platforms)-2)
        y= random.randint(platforms[x].getRect().left+10, platforms[x].getRect().right-10)
        coins.append( coin(y,platforms[x].getRect().top-10, 10, 10))

    ending= 0
    while True:
        if donkey.checkCollision(player.getRect()) :
                player.lives -= 1
                player.score -= 25
                if player.lives==0:
                    showGameOver()
                    ending=1
                reset(mySurf, player, donkey, queen)


        for i in fireballs:
            if i.checkCollision(player.getRect()):
                player.lives -= 1
                player.score -=25
                if player.lives== 0:
                    showGameOver()
                    ending=1
                reset(mySurf, player, donkey, queen)

        if queen.checkCollision(player.getRect()):
            player.score += 50
            del coins[:]
            for i in range(20):
                x= random.randint(0,len(platforms) -2)
                y= random.randint(platforms[x].getRect().left+10, platforms[x].getRect().right-10)
                coins.append(coin(y, platforms[x].getRect().top-10, 10, 10))
            reset(mySurf, player, donkey, queen)
                            
        pressed= pygame.key.get_pressed()
        donkey.move()
        flag=1
        rlist=[]
        for i in range(len(fireballs)):
            flag=fireballs[i].move(mySurf, platforms,ladders)
            if fireballs[i].isjumping==1:
                fireballs[i].jump(platforms, mySurf)
            if flag==0:
                flag=1
                rlist.append(i)

        for i in rlist:
            del fireballs[i]

        if donkey.getRect().right >= 300:
            fireballs.append( Fireball(donkey.getRect().right, donkey.getRect().bottom-10, 10, 10))
        if pressed[K_d] :
            player.moveRight(mySurf,platforms)

        if pressed[K_a]:
            player.moveLeft(mySurf,platforms)

        if pressed[K_w] :
            player.moveUp(mySurf,ladders)

        if pressed[K_s]:
            player.moveDown(mySurf,ladders)

        if pressed[K_SPACE]:
            if player.isjumping==0 and player.direction != 'up' and player.direction!= 'down':
                player.isjumping = 1
                player.yvel = -12
            
        if player.isjumping == 1:
            player.jump(platforms,mySurf)
        
        rlist=[]
        for i in range(len(coins)):
            if coins[i].checkCollision(player.getRect()):
                player.score += 5
                rlist.append(i)
        for i in rlist:
            del coins[i]

        for event in pygame.event.get():
            if  event.type==QUIT:
                pygame.quit()
                sys.exit()
           
            if event.type==KEYDOWN:
                if event.key== K_q:
                    pygame.quit()
                    sys.exit()
        if ending==0:
            set_display(mySurf, player, donkey, queen)
       
        pygame.display.update()
        fpsClock.tick(FPS)

#To set the board and characters at each iteration

def set_display(mySurf, player, donkey, queen):
    mySurf.draw()
    player.draw(mySurf)
    donkey.draw(mySurf)
    queen.draw(mySurf)
    for i in ladders:
        i.draw(mySurf)
    for i in platforms:
        i.draw(mySurf)
    for i in coins:
        i.draw(mySurf)
    for i in fireballs:
        i.draw(mySurf)

    font= pygame.font.Font(None, 36)
    text= font.render("score:  "+str(player.score), 1, (10,10,10))
    textpos= text.get_rect(centerx= mySurf.width -200)
    text3= font.render("lives: " +str(player.lives), 1, (10,10,10))
    textpos3= text.get_rect(centerx= xmargin+100)
    mySurf.screen.blit(text, textpos)
    mySurf.screen.blit(text3, textpos3)

#To reset the player after he touches donkey , player or queen to reset player's positioin

def reset(mySurf, player, donkey, queen):
    del fireballs[:]
    player.posx= xmargin+5
    player.posy= boardHeight -ymargin- 20
    set_display(mySurf, player, donkey, queen)

#To Show the screen after the game over

def showGameOver():
    mySurf.screen.fill(black)
    while True:

        for event in pygame.event.get():
            if  event.type==QUIT:
                pygame.quit()
                sys.exit()
           
            if event.type==KEYDOWN:
                if event.key== K_q:
                    pygame.quit()
                    sys.exit()

        font= pygame.font.Font(None, 40)
        text= font.render(" GAME OVER ", 2, (255,255,255))
        textpos= text.get_rect()
        textpos.centerx, textpos.centery= mySurf.width/2 , mySurf.height/2
        text1= font.render(" Final Score :  "+ str(player.score), 1, (255,255,255))
        textpos1= text.get_rect(centery= (mySurf.height)/2 + 40 , centerx= mySurf.width/2 -10)
        mySurf.screen.blit(text, textpos)
        mySurf.screen.blit(text1, textpos1)
        pygame.display.update()
        fpsClock.tick(FPS)

#To Show the starting screen of the game

def welcome():
    mySurf.screen.fill(black)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    return 
        font= pygame.font.Font(None, 40) 
        text= font.render(" CONTROLS ", 2, (255,255,255))
        textpos= text.get_rect( centery= (mySurf.height)/2-110 , centerx= mySurf.width/2 )
        text2= font.render(" w - moveup ", 1, (255,255,255))
        text4= font.render(" s- movedown ",1, (255,255,255))
        text5= font.render(" d- moveright ", 1, (255,255,255))
        text6= font.render(" a- moveleft ",1,(255,255,255))
        textpos2= text2.get_rect(centery = mySurf.height/2 - 70, centerx= mySurf.width/2 )
        textpos4= text4.get_rect(centery = mySurf.height/2 - 40, centerx= mySurf.width/2 )
        textpos5= text5.get_rect(centery = mySurf.height/2 - 10, centerx= mySurf.width/2 )
        textpos6= text6.get_rect(centery = mySurf.height/2 + 15, centerx= mySurf.width/2 )
        text3= font.render(" Press SPACE to begin ", 1, (255,255,255))
        textpos3= text3.get_rect(centery = mySurf.height -100, centerx= mySurf.width/2)
        mySurf.screen.blit(text, textpos)
        mySurf.screen.blit(text2, textpos2)
        mySurf.screen.blit(text3, textpos3)
        mySurf.screen.blit(text4, textpos4)
        mySurf.screen.blit(text5, textpos5)
        mySurf.screen.blit(text6, textpos6)
        pygame.display.update()
        fpsClock.tick(FPS)
