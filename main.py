from Tkinter import *
import numpy
import random

#for debugging purposes
import pdb

SCREEN_WIDTH = 400
NUM_WALLS = 3
DIST_BETWEEN_WALLS = 200
SCREEN_HEIGHT = NUM_WALLS*DIST_BETWEEN_WALLS
WALL_WIDTH = SCREEN_WIDTH
WALL_HEIGHT = 20
GAP_WIDTH = 100
DOWNWARDS_VELOCITY = 2
FLAPPER_SIZE = 30
FPS = 60.0
TERMINAL_VELOCITY = 20

#HAMMER-OFFSET = 50

def main():
    global W #Tkinter made me do it. :(
    W = World()
    root = Tk()
    root.title("QCopters")
    root.geometry("400x600")
    root.title("QCopters")
    global CANVAS
    W.render = True
    CANVAS = Canvas(root, width = SCREEN_WIDTH, height = SCREEN_HEIGHT, highlightthickness = 0)
    CANVAS.pack()
    root.bind("<Button-1>", mousePressed)
    root.bind("<Button-2>", toggleRendering)
    root.bind("<s>", saveQ)
    root.bind("<r>", restoreQ)
    #root.bind("<p>", pause)
    #root.bind("<q>", quit)
    root.resizable(width=0, height = 0)
    timerFired()
    root.mainloop()


def timerFired():
    W.moveTick()
    if W.render:
        W.renderFrame()
    CANVAS.after(1, timerFired)

def mousePressed(CANVAS):
    W.flapper.flip()
    
def toggleRendering(CANVAS):
    W.render = not W.render
    
def saveQ(CANVAS):
    W.flapper.saveQ()

def restoreQ(CANVAS):
    W.flapper.restoreQ()
    
class World(object):
    def __init__(self):
        self.highscore = 0
        self.averages = [0 for i in xrange(20)]
        self.average = 0
        self.score = 0
        self.reset()
        
    def reset(self):
        self.flapper = Flapper()
        self.walls = [Wall(DIST_BETWEEN_WALLS+n) for n in [0, DIST_BETWEEN_WALLS, -DIST_BETWEEN_WALLS]]
        self.averages.append(self.score)
        self.averages.pop(0)
        self.average = sum(self.averages)/20.0
        self.time = 0
        self.score = 0
        
    def incrementScore(self):
        self.score += 1
        self.highscore = max(self.score, self.highscore)
            
        
    def renderFrame(self):
        CANVAS.delete(ALL)
        CANVAS.create_text(0, 0, text = "Score: %d" % self.score, anchor = NW)
        CANVAS.create_text(SCREEN_WIDTH, 0, text = "Top: %d" % self.highscore, anchor = NE)
        CANVAS.create_text(SCREEN_WIDTH/2, 0, text = "Avg: %d" % self.average, anchor = N)
        for item in self.walls:
            item.render()
        self.flapper.render()
        
    def moveTick(self):
        self.time += 1
#    These two lines exist to verify that turning off rendering speeds things up.
#        if self.time % 100 == 0:
#            print self.time

#   To kill the AI, comment out lines 84, 85, and 89
        if self.time % 3 == 0:
            self.flapper.moveTick()
            if self.flapper.act(self.getLowestWall(), True):
                self.flapper.flip()
        for item in self.walls:
            item.moveTick()
            if item.intersectsWith(self.flapper) or self.flapper.outOfBounds():
                self.flapper.act(self.getLowestWall(), False)
                self.reset()
    
    def getLowestWall(self):
        bottom = self.walls[0]
        for item in self.walls:
            if item.centerY > bottom.centerY:
                bottom = item
        return bottom

class Sprite(object):
    def __init__(self, centerX, centerY):
        self.centerX = centerX
        self.centerY = centerY
    # def intersectsWith(self, a_Sprite):
    #     #return true or false
    #     pass
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
    x = (a1 < b1 < a2) or (b1 < a1 < b2)
    return x

class Flapper(Rectangle):
    #Put static variables here
    #All knowledge variables (Q matrix, parameters) are static and shared among all Flapper instances
    #Fields
    #   Action: 2
    #   Direction: 2
    #   Velocity: 15
    #   Vertical Distance: 10
    #   Horizontal Distance: 20
    #   State Space: 2*2*20*20*10 = 16k
    N_tap_div = 2
    N_acc_div = 2
    N_vel_div = 20
    N_h_div = 20
    N_v_div = 10

    tap_div = numpy.array([0, 1])
    acc_div = numpy.array([-2, 2])
    max_vel = numpy.sqrt(2*2*SCREEN_WIDTH)
    vel_div = numpy.linspace(-numpy.sqrt(max_vel), numpy.sqrt(max_vel), N_vel_div)**2
    vel_div[:N_vel_div/2] *= -1
    #1/2 a t^2 = x
    #1/2*2*t^2 = 400
    #t = 20
    #a t = v
    #v = 2*20 = 40
    
    #solution:
    #t = sqrt(2x/a)
    #v = sqrt(2xa)
    h_div = numpy.linspace(-(SCREEN_WIDTH-GAP_WIDTH), SCREEN_WIDTH-GAP_WIDTH, N_h_div)
    max_v = (SCREEN_HEIGHT - NUM_WALLS*WALL_HEIGHT)/NUM_WALLS
    v_div = numpy.linspace(0, max_v, N_v_div)
    #The actual Q matrix (knowledge base)
    #Q[direction, velocity, x distance to
    Q = numpy.zeros([N_tap_div, N_acc_div, N_vel_div, N_h_div, N_v_div])
    
    #learning parameters
    alpha = 0.7 # learning rate
    lam = 1.0 #discount rate (permanent memory)
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
        h = self.centerX - near_wall.centerX
        h_index = numpy.abs(self.h_div - h).argmin()
        v = near_wall.centerY + WALL_HEIGHT/2
        v_index = numpy.abs(self.v_div - v).argmin()
        
        #determine action
        #new_param = [acc_index, vel_index, h_index, v_index]
        #for some unknown reason, : slicing on the first argument doesn't work
        #Calling self.Q[:, new_param] breaks.
        #pdb.set_trace()
        new_param = ([0,1], acc_index, vel_index, h_index, v_index)
        #tap = self.Q[:, new_param].argmax()
        tap = self.Q[new_param].argmax()
        #update Q matrix
        if self.old_param != []:
            reward = 1 if life else -1000
            #self.Q[self.old_param] += alpha * (reward + lam*np.max(self.Q[:, new_param]) - self.Q[self.old_param])
            self.Q[self.old_param] += self.alpha * (reward + self.lam*numpy.max(self.Q[new_param]) - self.Q[self.old_param])
        
        self.old_param = (tap, acc_index, vel_index, h_index, v_index)
        #return action
        #0 for wait, 1 for tap (change direction of acceleration)
        
        return tap

    def flip(self):
        self.accel = -self.accel
        
    def outOfBounds(self):
        return not (FLAPPER_SIZE / 2 < self.centerX  < SCREEN_WIDTH - (FLAPPER_SIZE/2))
    
    def saveQ(self):
        print "SAVED!"
        numpy.save("Q_matrix.npy", self.Q)
    
    def restoreQ(self):
        print "RESTORED!"
        self.Q = numpy.load("Q_matrix.npy")
#class Hammer(Sprite):
    #plus direction swinging
    #and angle if we have time for that and can figure out how to do it nicely in pygame

class Wall(Sprite):
    def __init__(self, y):
        self.centerX = random.randint(GAP_WIDTH/2, SCREEN_WIDTH - GAP_WIDTH/2)
        self.centerY = y
        self.leftWall = Rectangle(self.centerX - GAP_WIDTH/2 - WALL_WIDTH/2, y, WALL_WIDTH, WALL_HEIGHT)
        self.rightWall = Rectangle(self.centerX + GAP_WIDTH/2 + WALL_WIDTH/2, y, WALL_WIDTH, WALL_HEIGHT)
    
    def render(self):
        self.leftWall.render()
        self.rightWall.render()
    
    def intersectsWith(self, rect):
        return self.leftWall.intersectsWith(rect) or self.rightWall.intersectsWith(rect)
    
    
    def moveTick(self):
        self.centerY += DOWNWARDS_VELOCITY
        if self.centerY - WALL_HEIGHT/2 > SCREEN_HEIGHT:
            self.centerY -= SCREEN_HEIGHT
            self.centerX = random.randint(GAP_WIDTH/2, SCREEN_WIDTH - GAP_WIDTH/2)
            self.centerX = random.randint(GAP_WIDTH/2, SCREEN_WIDTH - GAP_WIDTH/2)
            self.leftWall.centerX = self.centerX - GAP_WIDTH/2 - WALL_WIDTH/2
            self.rightWall.centerX = self.centerX + GAP_WIDTH/2 + WALL_WIDTH/2
            W.incrementScore()
        self.leftWall.centerY = self.centerY
        self.rightWall.centerY = self.centerY


if __name__ == "__main__":
    main()