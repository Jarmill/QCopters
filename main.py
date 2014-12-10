from Tkinter import *
import numpy
import random

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
WALL_WIDTH = SCREEN_WIDTH
WALL_HEIGHT = 20
GAP_WIDTH = 100
DOWNWARDS_VELOCITY = 2
FLAPPER_SIZE = 30
NUM_WALLS = 8
FPS = 60.0
TERMINAL_VELOCITY = 10
RENDER = True

#HAMMER-OFFSET = 50

def main():
    global W #Tkinter made me do it. :(
    W = World()
    if RENDER:
        root = Tk()
        root.title("QCopters")
        root.geometry("400x600")
        root.title("QCopters")
        global CANVAS
        CANVAS = Canvas(root, width = SCREEN_WIDTH, height = SCREEN_HEIGHT, highlightthickness = 0)
        CANVAS.pack()
        root.bind("<Button-1>", mousePressed)
        root.resizable(width=0, height = 0)
        timerFired()
        root.mainloop()
    else:
        while 1:
            W.moveTick()

def timerFired(): #Run if we're rendering; otherwise, just moveTick is run.
    W.moveTick()
    W.render()
    CANVAS.after(1, timerFired)

def mousePressed(CANVAS):
    W.flapper.flip()

class World(object):
    def __init__(self):
        self.flapper = Flapper()
        self.walls = [Wall(SCREEN_WIDTH/2, 200+n) for n in [-100, 100, 300]]
        self.time = 0
        
    def render(self):
        CANVAS.delete(ALL)
        for item in self.walls:
            item.render()
        self.flapper.render()
        
    def moveTick(self):
        self.time += 1
        if self.time % 3 == 0:
            self.flapper.moveTick()
        for item in self.walls:
            item.moveTick()
            if item.intersectsWith(self.flapper):
                print "LOSS"

class Sprite(object):
    def __init__(self, centerX, centerY):
        self.centerX = centerX
        self.centerY = centerY
    def intersectsWith(self, a_Sprite):
        #return true or false
        pass
    #def getBounds():
    #returns ((x, y), (x, y)) for top left and bottom right corners

class Rectangle(Sprite):
    def __init__(self, centerX, centerY, width, height):
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height
        
        
    def render(self):
        #CANVAS.create_rectangle(self.getLeftSide(), self.getTop()-4, self.getRightSide(), self.getBottom(), fill="white", width=0)
        CANVAS.create_rectangle(self.getLeftSide(), self.getTop(), self.getRightSide(), self.getBottom(), fill="grey80", width=0)
        
    def moveDownBy(self, dist):
        self.centerY += dist
        if self.centerY > SCREEN_HEIGHT + WALL_HEIGHT/2:
            self.centerY -= SCREEN_HEIGHT
        
    def getRightSide(self):
        return self.centerX + self.width/2
    def getLeftSide(self):
        return self.centerX - self.width/2
    def getTop(self):
        return self.centerY - self.height/2
    def getBottom(self):
        return self.centerY + self.height/2
        
    def intersectsWith(self, a_Rectangle):
        return intersects(self.getLeftSide(), self.getRightSide(), a_Rectangle.getLeftSide(), a_Rectangle.getRightSide()) and intersects(self.getTop(), self.getBottom(), a_Rectangle.getTop(), a_Rectangle.getBottom())

def intersects(a1, a2, b1, b2):
    return a1 < b1 < a2 or b1 < a1 < b2

class Flapper(Rectangle):
    #Put static variables here
    #All knowledge variables (Q matrix, parameters) are static and shared among all Flapper instances
    #Fields
    #   Action: 2
    #   Direction: 2
    #   Velocity: 15
    #   Vertical Distance: 10
    #   Horizontal Distance: 20
    #   State Space: 2*2*20*10*20 = 12k
    N_tap_div = 2
    N_acc_div = 2
    N_vel_div = 20
    N_h_div = 25
    N_v_div = 10
    #TODO: figure out a way to incorporate the action with the acceleration
    tap_div = numpy.array([0, 1])
    acc_div = numpy.array([-2, 2])
    vel_div = numpy.linspace(-numpy.sqrt(40), numpy.sqrt(40), N_vel_div)**2
    #1/2 a t^2 = x
    #1/2*2*t^2 = 400
    #t = 20
    #a t = v
    #v = 2*20 = 40
    #might want to make vel nonlinearly spaced, like quadratic spacing.
    #low velocities are more likely than high velocities.
    h_div = numpy.linspace(-(SCREEN_WIDTH-GAP_WIDTH), SCREEN_WIDTH-GAP_WIDTH, N_h_div)
    v_div = numpy.linspace(0, (SCREEN_HEIGHT - NUM_WALLS*WALL_HEIGHT)/NUM_WALLS, N_v_div),
    #The actual Q matrix (knowledge base)
    #Q[direction, velocity, x distance to
    Q = numpy.zeros([N_tap_div, N_acc_div, N_vel_div, N_h_div, N_v_div])
    
    def __init__(self):
        self.accel = 2
        self.centerX = SCREEN_WIDTH / 2
        self.centerY = SCREEN_HEIGHT - FLAPPER_SIZE
        self.width = FLAPPER_SIZE
        self.height = FLAPPER_SIZE
        self.velocity = 0
        self.old_param = []
    
    def moveTick(self):
        #moveTick is for rendering/interaction with world only
        if self.accel >= 0:
            self.velocity = min(self.velocity + self.accel, TERMINAL_VELOCITY)
        else:
            self.velocity = max(self.velocity + self.accel, -TERMINAL_VELOCITY)
        self.centerX += self.velocity

    def act(self, near_wall, life):
        #actual implementation of Q-Learning
        
        #gather relevant parameters
        acc = self.accel
        acc_index = numpy.abs(self.acc_div - acc).argmin()
        vel = self.velocity
        vel_index = numpy.abs(self.vel_div - vel).argmin()
        h = self.x - near_wall.centerX
        h_index = numpy.abs(self.h_div - h).argmin()
        v = near_wall.centerY + WALL_HEIGHT/2
        v_index = numpy.abs(self.v_div - v).argmin()
        
        #determine action
        new_param = [acc_index, vel_index, h_index, v_index]
        tap = self.Q[:, new_param].argmax()
        
        #update Q matrix
        if self.old_param != []:
            reward = 1 if life else -1000
            self.Q[self.old_param] += alpha * (reward + lam*np.max(self.Q[:, new_param]) - self.Q[self.old_param])
            alpha = 0.7 # learning rate
            lam = 1.0 #discount rate (permanent memory)
        
        self.old_param = [tap, acc_index, vel_index, h_index, v_index]
        #return action
        #0 for wait, 1 for tap (change direction of acceleration)
        
        return tap

    def flip(self):
        self.accel = -self.accel

#class Hammer(Sprite):
    #plus direction swinging
    #and angle if we have time for that and can figure out how to do it nicely in pygame

class Wall(Sprite):
    def __init__(self, x, y):
        self.centerX = x
        self.centerY = y
        self.leftWall = Rectangle(self.centerX - GAP_WIDTH/2 - WALL_WIDTH/2, y, WALL_WIDTH, WALL_HEIGHT)
        self.rightWall = Rectangle(self.centerX + GAP_WIDTH/2 + WALL_WIDTH/2, y, WALL_WIDTH, WALL_HEIGHT)
    
    def render(self):
        self.leftWall.render()
        self.rightWall.render()
    
    def moveTick(self):
        self.centerY += DOWNWARDS_VELOCITY
        if self.centerY - WALL_HEIGHT/2 > SCREEN_HEIGHT:
            self.centerY -= SCREEN_HEIGHT
            self.centerX = random.randint(GAP_WIDTH/2, SCREEN_WIDTH - GAP_WIDTH/2)
            self.leftWall.centerX = self.centerX - GAP_WIDTH/2 - WALL_WIDTH/2
            self.rightWall.centerX = self.centerX + GAP_WIDTH/2 + WALL_WIDTH/2
        self.leftWall.centerY = self.centerY
        self.rightWall.centerY = self.centerY


if __name__ == "__main__":
    main()