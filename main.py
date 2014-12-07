# Pseudocode for Swing Copters
# Still missing: exact details of where we actually do the Q-Learning
# Translation into actual python ongoing
import tkinter
import numpy
import random

SCREEN-WIDTH = 400
SCREEN-WIDTH = 600
WORLD = world()
GAP-WIDTH = 100
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
    
    
class Flapper(Sprite):
    #all the aspects of our item

#class Hammer(Sprite):
    #plus direction swinging
    #and angle if we have time for that and can figure out how to do it nicely in pygame

class Wall(Sprite):
    def __init__(self, x, y):
        super(Wall, Sprite).__init__()
        self.leftWall = Rectangle(x - GAP-WIDTH - WALL-WIDTH, y, WALL-WIDTH, WALL-HEIGHT)
        self.rightWall = Rectangle(x + GAP-WIDTH, y, WALL-WIDTH, WALL-HEIGHT)
    
    def render():
        self.leftWall.render()
        self.rightWall.render()



if __name__ == "__main__":
    main()