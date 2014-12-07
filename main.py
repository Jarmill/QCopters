# Pseudocode for Swing Copters
# Still missing: exact details of where we actually do the Q-Learning
# Translation into actual python ongoing
import tkinter
import numpy
import random

SCREEN_WIDTH = 400
SCREEN_WIDTH = 600
WALL_WIDTH = SCREEN_WIDTH
WALL_HEIGHT = 20
GAP_WIDTH = 100
DOWNWARDS_VELOCITY = 1
FPS = 60.0

#HAMMER-OFFSET = 50

def main(argv=None):
    if argv is None:
        argv = sys.argv
    #set the boolean variable RENDER, which has been passed in
    #set the parameters for various configuration things
    #make a screen
    #run loop: (could maybe be broken into its own function)
        #process input
        #update locations of Sprites; also their fields
            #if things go off the bottom of the screen, we make new ones higher up.
            #check for loss
        #update weights
        if render:
            WORLD.render()

class world():
    def __init__(self):
        pass
    def render(self):
        pass
    def moveTick(self):
        pass

class Sprite():
    def __init__(self, centerX, centerY):
        self.centerX = centerX
        self.centerY = centerY
    def intersectsWith(a_Sprite):
        #return true or false
        return true
    #def getBounds():
    #returns ((x, y), (x, y)) for top left and bottom right corners

class Rectangle(Sprite):
    def __init__(self, topX, leftY, width, height):
        self.centerX = topX - (width / 2)
        self.centerY = leftY - (height / 2)
        self.width = width
        self.height = height
        #Tkinter rectangle goes here
    def render(self):
        pass
    def moveDownBy(dist):
        self.centerY += dist
    
    
class Flapper(Sprite):
    def __init__(self):
        self.accel = 2
        self.x = SCREEN_WIDTH / 2
        self.velocity = 0
    
    def update(self):
        self.velocity += self.accel
        self.x += self.velocity


    def flip(self):
        self.accel = -self.accel
    
    def render(self):
        pass

#class Hammer(Sprite):
    #plus direction swinging
    #and angle if we have time for that and can figure out how to do it nicely in pygame

class Wall(Sprite):
    def __init__(self, x, y):
        super(Wall, Sprite).__init__()
        self.leftWall = Rectangle(x - GAP_WIDTH - WALL_WIDTH, y, WALL_WIDTH, WALL_HEIGHT)
        self.rightWall = Rectangle(x + GAP_WIDTH, y, WALL_WIDTH, WALL_HEIGHT)
    
    def render(self):
        self.leftWall.render()
        self.rightWall.render()
    
    def update(self):
        self.leftWall.moveDownBy(DOWNWARDS_VELOCITY)
        self.rightWall.moveDownBy(DOWNWARDS_VELOCITY)


if __name__ == "__main__":
    main()