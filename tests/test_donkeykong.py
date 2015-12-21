from main import *
from classes import *
from functions import *
from pygame.locals import *
from constants import *

class Testclass:
    def test_person(self):
        mySurf=Board(boardHeight, boardWidth, bgColor, xmargin, xmargin, ymargin, ymargin)
        player= Player(xmargin+5, boardHeight-ymargin-20, 20, 10)
        def check_player_spawn():
            (x,y)= player.getCoords()
            assert x==xmargin+5 and y== boardHeight-ymargin-20
        
        def check_player_moveRight():
            player.moveRight(mySurf, platforms)
            (x,y) = player.getCoords()
            assert x==xmargin+10 and y== boardHeight-ymargin-20

        def check_player_moveLeft():
            player.moveLeft(mySurf, platforms)
            (x,y) = player.getCoords()
            assert x== xmargin+5 and y== boardHeight-ymargin-20

        def check_player_jump():
            player.jump(platforms, mySurf)
            (x,y) = player.getCoords()
            assert x== xmargin+5 and y== boardHeight- ymargin-20

        check_player_spawn()
        check_player_moveRight()
        check_player_moveLeft()
        check_player_jump()

    def test_donkey(self):
        donkey= Donkey(xmargin+5, ymargin+gapBetweenLadders+30, 30, 20)
        def check_donkey_spawn():
            (x,y)= donkey.getCoords()
            assert x==xmargin+5 and y== ymargin+gapBetweenLadders+30

        def check_donkey_move():
            x= 100
            while x>0 :
                donkey.move()
                x= x-1

            (x,y) = donkey.getCoords()
            assert x> xmargin and y== ymargin+gapBetweenLadders+30


        check_donkey_spawn()
        check_donkey_move()

    def test_player(self):
        player= Player(xmargin+5, boardHeight-ymargin-20, 20, 10)
        def check_player_lives():
            assert player.lives==3

        check_player_lives()

    def test_fireball(self):
        donkey=Donkey(xmargin+5, ymargin+gapBetweenLadders+30, 30, 20)
        fireball= Fireball(donkey.getRect().right, donkey.getRect().bottom-10, 10, 10)
        mySurf=Board(boardHeight, boardWidth, bgColor, xmargin, xmargin, ymargin, ymargin)
        def check_fireball_move():
            x=1000
            while x>0:
                fireball.move(mySurf, platforms, ladders)
                x= x-1

            (x,y) = fireball.getCoords()
            assert x> xmargin and x< boardWidth and y> ymargin

        check_fireball_move()

    def test_ladders(self):
        mySurf=Board(boardHeight, boardWidth, bgColor, xmargin, xmargin, ymargin, ymargin)
        player= Player(xmargin+5, boardHeight-ymargin-20, 20, 10)
        countr= 1000
        flag=0
        def check_collision_ladder():
            flag=0
            while countr>0:
                for i in ladders:
                    if i.checkCollision(player.getRect()):
                        flag=1
                        break
                if flag==1 :
                    break

                player.moveRight(mySurf, platforms)

            assert countr> 0

        check_collision_ladder()

    def test_coins(self):
        coins=[]
        for i in range(20):
            x= random.randint(0,len(platforms)-2)
            y= random.randint(platforms[x].getRect().left+10, platforms[x].getRect().right-10)
            coins.append( coin(y,platforms[x].getRect().top-10, 10, 10))

        donkey=Donkey(xmargin+5, ymargin+gapBetweenLadders+30, 30, 20)
        fireball= Fireball(donkey.getRect().right, donkey.getRect().bottom-10, 10, 10)
        mySurf=Board(boardHeight, boardWidth, bgColor, xmargin, xmargin, ymargin, ymargin)
        def check_coins_collision():
            countr=1000

            while countr> 0:
                flag=0
                fireball.move(mySurf, platforms, ladders)
                for i in coins:
                    if i.checkCollision(fireball.getRect()):
                        flag=1
                        break
                if flag==1:
                    break
                countr= countr-1

            assert countr>0

        check_coins_collision()

        
        




            


