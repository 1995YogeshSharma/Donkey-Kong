#!/usr/bin/python

import random
import sys, pygame
from pygame.locals import *
from constants import *

#Consists of motion controls and common variables for classes derived from it

class Person():
    def __init__(self,x,y,a,b):
        self.yvel= 0
        self.posx= x
        self.posy= y
        self.height= a
        self.width= b
        self.isjumping= 0
        self.direction= 'right'

    def getCoords(self):            #gives coordinates of the object
        return (self.posx, self.posy)

    def getDirection(self):         #gives the direction in which object is moving
        return self.direction

    def getRect(self):              #gives a rect object for the object
        return pygame.Rect(self.posx, self.posy, self.width, self.height)

    def checkCollision(self, rect): #Checks collision with rect object
        return rect.colliderect(self.getRect())

    def moveRight(self,mySurf,platforms):  #moves the object right
        if self.direction!='down' and self.direction!='up':
            if self.posx + 15 < mySurf.width - xmargin :
                self.posx += 5
                self.direction='right'
                flag=0
                for i in platforms:
                    p=i.getRect()
                    if (self.posx>p.right or self.posx < p.left) and self.getRect().bottom == p.top:
                        flag=1
                        break
                if  flag==1:
                    self.isjumping =1
                

    def moveLeft(self,mySurf,platforms):    #moves the object left
        if self.direction!='down' and self.direction!='up':
            if self.posx -5 > xmargin:
                self.posx -= 5
                self.direction='left'
                flag=0
                for i in platforms:
                    p= i.getRect()
                    r= self.getRect()
                    if (r.right > p.right or r.left< p.left) and r.bottom == p.top:
                        flag=1
                        break
                if flag==1:
                    self.isjumping=1

    def moveDown(self, mySurf,ladders):  #moves the object down
        for i in range(len(ladders)):
            if ladders[i].checkCollision(self.getRect()):
                p= ladders[i].getRect()
                if self.posy+self.height +5< p.bottom :
                    self.posy += 5
                    self.direction= 'down'
                elif self.posy+self.height+5 >= p.bottom:
                    self.posy= p.bottom -self.height
                
                if self.posy + self.height == p.bottom and i!=3 and i!=5 and i!=9:
                    self.direction= 'stable'

    def moveUp(self, mySurf, ladders):  #moves the object up
        for j in range(len(ladders)):
            if ladders[j].checkCollision(self.getRect()):
                p= ladders[j].getRect()
                if self.posy+self.height-5 > p.top:
                    self.posy-=5
                    self.direction= 'up'
                elif self.posy+self.height-5 <= p.top:
                    self.posy= p.top- self.height-ladderWidth
                if self.posy + self.height == p.top-ladderWidth and j!=2 and j!=4 and j!=8:
                    self.direction='stable'

    def jump(self,platforms,mySurf):    #makes the object jump or fall using concept of y-velocity and gravity
        self.yvel += gravity
        self.posy+=self.yvel

        for i in platforms:
            if i.checkCollision(self.getRect()) :
                p= i.getRect()
                self.posy = p.top-self.height
                self.yvel=0
                self.isjumping=0
                return

class Board():                  #defines the main board of the game
    def __init__(self, h, w, color, ml, mr, mt, mb):
        self.height= h
        self.width= w
        self.color= color
        self.margin_left= ml
        self.margin_right= mr
        self.margin_top= mt
        self.margin_bottom= mb
        self.screen= pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("DONKEY KONG")

    def draw(self):             #draws board
        self.screen.fill(self.color)
        pygame.draw.rect(self.screen , red, (xmargin, ymargin, boardWidth-2*xmargin, boardHeight-2*ymargin))

class Player(Person):        #main character
    def __init__(self, x,y,a,b):
        Person.__init__(self,x,y,a,b)
        self.score= 0
        self.limit_y=0
        self.lives= 3

    def draw(self,mySurf):
        pygame.draw.rect(mySurf.screen, green, self.getRect())


class Donkey(Person):     #defines queen and donkey
    def __init__(self, x,y,a,b):
        Person.__init__(self,x,y,a,b)
        self.state=1

    def draw(self, mySurf):
        pygame.draw.rect(mySurf.screen, blue, self.getRect())

    def move(self):      #To automate donkey's motion
        a=self.getRect()
        if self.direction == 'left':
            if a.right < 300:
                self.posx+=3
            else:
                self.direction= 'right'

        elif self.direction== 'right':
            if a.left >xmargin+5:
                self.posx-=4
            else:
                self.direction= 'left'

class Ladder():         #defines all the ladder in the game
    def __init__(self, (startx,starty), (endx,endy)):
        self.startx= startx
        self.starty= starty
        self.endx,self.endy= endx,endy

    def getCoords(self):  #give coordinates of the ladder
        return ((self.startx, self.starty), (self.endx, self.endy))

    def getRect(self):    #gives ladder as a rect object
        return pygame.Rect( self.startx, self.endy, ladderWidth, self.starty- self.endy )

    def draw(self, mySurf):
        pygame.draw.line(mySurf.screen, black, (self.startx, self.starty), (self.endx, self.endy))
        pygame.draw.line(mySurf.screen, black, (self.startx+15,self.starty),(self.endx+15, self.endy))
        i= self.starty
        while i > self.endy:
            pygame.draw.line(mySurf.screen, black, (self.startx,i), (self.startx+15,i))
            i=i-10

    def checkCollision(self, rect):   #checks collision of ladder with rect object
       if rect.right > self.startx and rect.left < self.startx+15 :
           if rect.bottom <= self.starty and rect.bottom+ladderWidth >= self.endy:
               return 1
       return 0

    def getLength(self):            #gives length of ladder
        return self.starty- self.endy
    
class coin(Person):                 #defines the coins in the game
    def __init__(self, x, y, width, height):
        Person.__init__(self, x, y, width, height)

    def draw(self, mySurf):
        a= self.getRect()
        pygame.draw.circle(mySurf.screen, gold, a.center, self.height/2)

    def checkCollision(self, rect):   #checks collision of coin with a rect object
        a= self.getRect()
        if a.colliderect(rect):
            return 1
        return 0

class Fireball(Person):     #defines all the fireball in the game
    def __init__(self, x, y, a, b):
        Person.__init__(self, x, y, a, b)

    def draw(self, mySurf):
        a= self.getRect()
        pygame.draw.rect(mySurf.screen, fire_color, a)

    def move(self,mySurf,platforms,ladders):        #automating fireballs motion 
        a = self.getRect()
        flag=0
        if a.bottom >= platforms[1].getRect().bottom and a.left <= xmargin +20:
            return 0
        for i in ladders :
            if i.checkCollision(a) and i.getLength() >= gapBetweenLadders-5  and a.top <= i.endy:
                x= random.randint(0,3)
                if x==0:
                    self.moveDown(mySurf, ladders)
                    flag=1

        if flag==0:
            if self.direction=='right':
                self.moveRight(mySurf, platforms)
                if self.posx >= mySurf.width -xmargin-15:
                    self.direction='left'
            elif self.direction== 'down':
                self.moveDown(mySurf, ladders)
            else:
                self.moveLeft(mySurf, platforms)
                if self.posx< xmargin+10:
                    self.direction='right'
        else:
            flag=0

     #  if self.direction== 'stable':
     #      x= random.randint(0,1)
     #      if x==1:
     #          self.direction= 'left'
     #      else :
     #          self.direction= 'right'
     #  for i in ladders:
     #      if i.checkCollision(a) and i.getLength() >= gapBetweenLadders :
     #          x= random.randint(0,1)
     #          if a.top>i.endy+15:
     #              if self.direction== 'right' or self.direction=='left':
     #                  break
     #          
     #          if x==1:
     #              if self.direction=='right':
     #                  self.moveRight(mySurf, platforms)
     #              else:
     #                  self.moveLeft(mySurf, platforms)
     #          else:
     #              self.moveDown(mySurf, ladders)
     #          flag=1
     #          break
     #  if flag==0:
     #      if self.direction=='right':
     #          self.moveRight(mySurf, platforms)
     #          if self.posx >= mySurf.width - xmargin-15:
     #              self.direction = 'left'
     #      else :
     #          self.moveLeft(mySurf, platforms)
     #          if self.posx <= xmargin+15:
     #              self.direction = 'right'
        return 1

class Platform():           #defines all the platforms in the game
    def __init__(self, posx, posy, width, height):
        self.posx= posx
        self.posy= posy
        self.width= width
        self.height= height

    def getRect(self):      #gives platforms as a rect object
        return pygame.Rect(self.posx, self.posy, self.width , self.height)

    def draw(self,mySurf):
        pygame.draw.rect(mySurf.screen, dark_green, self.getRect())
    
    def checkCollision(self, rect):  #checks collision of platform with a rect object
        p = self.getRect()
        if p.colliderect(rect):
            return 1
        else : return 0


