from Tkinter import *
import numpy
import random

#for debugging purposes
import pdb

SCREEN_WIDTH = 200
NUM_WALLS = 3
DIST_BETWEEN_WALLS = 100
SCREEN_HEIGHT = NUM_WALLS*DIST_BETWEEN_WALLS
WALL_WIDTH = SCREEN_WIDTH
WALL_HEIGHT = 15
GAP_WIDTH = 75
DOWNWARDS_VELOCITY = 2
FLAPPER_SIZE = 15
FPS = 60.0
TERMINAL_VELOCITY = 30
ACCEL = 2
COST = 1000

COLORS = ["Blue", "Red", "Green", "Yellow", "Grey60", "Orange", "Navy", "Purple", "Pink"]

def main():
    global W #Tkinter made me do it. :(
    W = World()
    root = Tk()
    root.title("QCopters")
    root.geometry("%dx%d"%(SCREEN_WIDTH,SCREEN_HEIGHT) )
    root.title("QCopters")
    global CANVAS
    W.render = True
    CANVAS = Canvas(root, width = SCREEN_WIDTH, height = SCREEN_HEIGHT, highlightthickness = 0)
    CANVAS.pack()
    #root.bind("<1>", mousePressed)
    root.bind("<2>", toggleRendering)
    root.bind("<s>", saveQ)
    root.bind("<r>", restoreQ)
    root.bind("<h>", humanModeToggle)
    root.bind("<v>", toggleRendering)
    #root.bind("<space>", mousePressed)
    root.bind("<p>", pause)
    root.bind("<q>", exit)
    root.bind("<d>", debug)
    root.resizable(width=0, height = 0)
    timerFired()
    root.mainloop()


def timerFired():
    if not W.paused:
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

def debug(CANVAS):
    W.debug()
    
class World(object):
    def __init__(self):
        self.highscore = 0
        self.averages = [0 for i in xrange(20)]
        self.weight = 0.4
        self.average = 0
        self.score = 0
        self.flappermode = True
        self.paused = False
        self.reset()
        
    def reset(self):
        self.flappers = [Flapper() for i in xrange(30)]
        self.walls = [Wall(n) for n in [DIST_BETWEEN_WALLS * k for k in range(0, NUM_WALLS)]]
        self.averages.append(self.score)
        self.averages.pop(0)
        self.average = sum(self.averages)/20.0
        #exponential moving average
        #self.average = self.weight * self.score + (1-self.weight) * self.average
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
        self.color = "black"
        for item in self.walls:
            item.render()
        for item in self.flappers:
            if not item.dead:
                item.render()
        
    def moveTick(self):
        self.time += 1
#    These two lines exist to verify that turning off rendering speeds things up.
#        if self.time % 100 == 0:
#            print self.time

        if self.time % 3 == 0:
            for item in self.flappers:
                item.moveTick()
            for item in self.flappers:
                if not item.dead:
                    if item.act(self.getLowestWall(), True):
                    #if item.flappermode:
                        item.flip()
        for item in self.walls:
            item.moveTick()
            for bird in self.flappers:
                if item.intersectsWith(bird) or bird.outOfBounds():
                    bird.act(self.getLowestWall(), False)
                    bird.dead = True
        if not False in [bird.dead for bird in self.flappers]:
            self.reset()
    
    def getLowestWall(self):
        bottom = self.walls[0]
        for item in self.walls:
            if item.centerY > bottom.centerY:
                bottom = item
        return bottom
    
    def debug(self):
        pdb.set_trace()
        
def pause(event):
    W.paused = not W.paused

def humanModeToggle(event):
    W.flappermode = not W.flappermode
    
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
        CANVAS.create_rectangle(self.getLeftSide(), self.getTop(), self.getRightSide(), self.getBottom(), fill="Black", width=0)
        
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
    #   Velocity: 16
    #   Horizontal Distance: 16
    #   Vertical Distance: 10
    #   Gap Distance: 10
    #   State Space: 2*12*13*8*5 = 12.5k
    N_tap_div = 2
    N_acc_div = 2
    N_vel_div = 12
    N_h_div = 11
    N_v_div = 8
    N_x_div = 5
    

    tap_div = numpy.array([0, 1])
    acc_div = numpy.array([-ACCEL, ACCEL])
    #max_vel = numpy.sqrt(2*2*SCREEN_WIDTH)
    #vel_div = numpy.linspace(-numpy.sqrt(max_vel), numpy.sqrt(max_vel), N_vel_div)**2
    vel_div = numpy.linspace(-numpy.sqrt(TERMINAL_VELOCITY), numpy.sqrt(TERMINAL_VELOCITY), N_vel_div)**2
    vel_div[:N_vel_div/2] *= -1
    h_div = numpy.linspace(-(SCREEN_WIDTH-GAP_WIDTH), SCREEN_WIDTH-GAP_WIDTH, N_h_div)
    v_div = numpy.linspace(0, DIST_BETWEEN_WALLS, N_v_div)
    x_div = numpy.array([0.1, 0.3, 0.5, 0.7, 0.9])*SCREEN_WIDTH

    #The actual Q matrix (knowledge base)
    #Q[direction, velocity, x distance to
    Q = numpy.zeros([N_tap_div, N_acc_div, N_vel_div, N_h_div, N_v_div, N_x_div])
    Q_count = numpy.zeros([N_tap_div, N_acc_div, N_vel_div, N_h_div, N_v_div, N_x_div])
    
    
    #learning parameters
    alpha = 0.6 # learning rate
    lam = 0.98 #discount rate (permanent memory)
    def __init__(self):
        self.accel = random.choice([-ACCEL, ACCEL])
        self.centerX = random.randint(3*FLAPPER_SIZE, SCREEN_WIDTH - 3*FLAPPER_SIZE)
        self.centerY = SCREEN_HEIGHT - FLAPPER_SIZE
        self.width = FLAPPER_SIZE
        self.height = FLAPPER_SIZE
        self.velocity = 0
        self.old_param = []
        self.dead = False
        self.color = random.choice(COLORS)

    
    def moveTick(self):
        #moveTick is for rendering/interaction with world only
        if self.accel >= 0:
            self.velocity = min(self.velocity + self.accel, TERMINAL_VELOCITY)
        else:
            self.velocity = max(self.velocity + self.accel, -TERMINAL_VELOCITY)
        self.centerX += self.velocity
    
    def render(self):
        CANVAS.create_rectangle(self.getLeftSide(), self.getTop(), self.getRightSide(), self.getBottom(), fill=self.color, width=0)
    
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
        x = self.centerX
        x_index = numpy.abs(self.x_div - x).argmin()
        
        #determine action
        #new_param = [acc_index, vel_index, h_index, v_index]
        #for some unknown reason, : slicing on the first argument doesn't work
        #Calling self.Q[:, new_param] breaks.
        #pdb.set_trace()
        new_param = ([0,1], acc_index, vel_index, h_index, v_index, x_index)
        #tap = self.Q[:, new_param].argmax()
        tap = self.Q[new_param].argmax()
        #update Q matrix
        if self.old_param != []:
            reward = 1 if life else -COST
            #self.Q[self.old_param] += alpha * (reward + lam*np.max(self.Q[:, new_param]) - self.Q[self.old_param])
            self.Q[self.old_param] += self.alpha * (reward + self.lam*numpy.max(self.Q[new_param]) - self.Q[self.old_param])
        
        self.old_param = (tap, acc_index, vel_index, h_index, v_index, x_index)
        self.Q_count[self.old_param] += 1
        #return action
        #0 for wait, 1 for tap (change direction of acceleration)
        
        #if tap: print new_param, self.Q[new_param]
        #if tap: print self.old_param, self.Q[self.old_param]
        return tap

    def flip(self):
        self.accel = -self.accel
        
    def outOfBounds(self):
        return not (FLAPPER_SIZE / 2 < self.centerX  < SCREEN_WIDTH - (FLAPPER_SIZE/2))
    
    def saveQ(self):
        print "SAVED!"
        numpy.save("Q_matrix.npy", self.Q)
        numpy.savetxt("Q_text.txt", self.Q.flatten())
        
    def restoreQ(self):
        print "RESTORED!"
        self.Q = numpy.load("Q_matrix.npy")
        #pdb.set_trace()

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