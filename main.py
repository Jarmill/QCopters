 # -*- coding: iso-8859-15 -*-
from Tkinter import *
import numpy
import random

SCREEN_WIDTH = 200
NUM_WALLS = 3
DIST_BETWEEN_WALLS = 150
SCREEN_HEIGHT = NUM_WALLS*DIST_BETWEEN_WALLS
WALL_WIDTH = SCREEN_WIDTH
WALL_HEIGHT = 15
GAP_WIDTH = 75
FLAPPER_SIZE = 15
FPS = 60.0
TERMINAL_VELOCITY = 30
ACCEL = 2
COST = 100000

COLORS = ["Blue", "Red", "Green", "Yellow", "Orange", "Navy", "Purple"]

def main():
    global W #Tkinter made me do it. :(
    W = World()
    root = Tk()
    root.title("QCopters")
    root.geometry("%dx%d"%(SCREEN_WIDTH+300,SCREEN_HEIGHT))
    root.title("QCopters")
    global CANVAS
    W.render = True
    CANVAS = Canvas(root, width = SCREEN_WIDTH + 300, height = SCREEN_HEIGHT, highlightthickness = 0)
    CANVAS.pack()
    root.bind("<1>", mousePressed)
    root.bind("<2>", toggleRendering)
    root.bind("<s>", saveQ)
    root.bind("<r>", restoreQ)
    root.bind("<a>", rainbow)
    root.bind("<h>", humanModeToggle)
    root.bind("<v>", toggleRendering)
    root.bind("<space>", mousePressed)
    root.bind("<p>", pause)
    root.bind("<q>", exit)
    root.bind("<d>", debug)
    root.bind("<n>", numFlappers)
    root.bind("<e>", epsilonZero)
    root.resizable(width=0, height = 0)
    timerFired()
    root.mainloop()


def timerFired():
    if not W.paused:
        W.moveTick()
        if W.render:
            W.renderFrame()
    if not W.HUMAN:
        CANVAS.after(1, timerFired)
    else:
        CANVAS.after(100, timerFired)

def mousePressed(CANVAS):
    if W.HUMAN:
        W.flappers[0].flip()

def epsilonZero(thunk):
    if Flapper.epsilon == 0:
        Flapper.epsilon = Flapper.epsilon_old
    else:
        Flapper.epsilon = 0

def humanModeToggle(thunk):
    W.HUMAN = not W.HUMAN

def numFlappers(thunk):
    W.numFlap =  (W.numFlap * 5) % 624
    W.reset()

def toggleRendering(CANVAS):
    W.render = not W.render
    
def saveQ(CANVAS):
    print "Saved Q Matrix"
    numpy.save("Q_matrix.npy", Flapper.Q)
    numpy.savetxt("Q_text.txt", Flapper.Q.flatten())
    
def restoreQ(CANVAS):
    print "Restored Q Matrix"
    Flapper.Q = numpy.load("Q_matrix.npy")

def debug(CANVAS):
    W.debug()

def rainbow(CANVAS):
    W.rainbow = not W.rainbow
    
class World(object):
    def __init__(self):
        self.numFlap = 1
        self.DOWNWARDS_VELOCITY = 6
        self.HUMAN = False
        self.ITERATIONS = 0
        self.rainbow = False
        self.highscore = 0
        self.averages = [0 for i in xrange(100)]
        self.weight = 0.4
        self.average = 0
        self.score = 0
        self.flappermode = True
        self.paused = False
        self.reset()
        
    def reset(self):
        self.flappers = [Flapper() for i in range(self.numFlap)]
        if self.HUMAN:
            self.flappers = [Flapper()]
        self.walls = [Wall(n) for n in [DIST_BETWEEN_WALLS * k for k in range(0, NUM_WALLS)]]
        self.averages[self.ITERATIONS % 100] = self.score
        if self.ITERATIONS % 100 == 0:
            self.sumOfHundred = sum(self.averages)
            print self.sumOfHundred
        #exponential moving average
        #self.average = self.weight * self.score + (1-self.weight) * self.average
        self.time = 0
        self.score = 0
        self.ITERATIONS += 1
        Flapper.alpha *= Flapper.alpha_decay
        Flapper.epsilon *= Flapper.epsilon_decay
        Flapper.epsilon_old *= Flapper.epsilon_decay
        
    def incrementScore(self):
        self.score += 1
        self.highscore = max(self.score, self.highscore)
            
        
    def renderFrame(self):
        CANVAS.delete(ALL)
        
        CANVAS.create_rectangle(-1, 0, SCREEN_WIDTH, SCREEN_HEIGHT, fill = "Grey90")
        self.color = "black"
        for item in self.walls:
            item.render()
        for item in self.flappers:
            if not item.dead:
                item.render()
        CANVAS.create_rectangle(SCREEN_WIDTH, 0, SCREEN_WIDTH + 300, SCREEN_HEIGHT, fill = "White")
        CANVAS.create_text(SCREEN_WIDTH + 15, 0, text = "Score: %d" % self.score, anchor = NW)
        CANVAS.create_text(SCREEN_WIDTH+300, 0, text = "Top: %d" % self.highscore, anchor = NE)
        #CANVAS.create_text(SCREEN_WIDTH+150, 0, text = "Moving Average: %d" % self.average, anchor = N)
        CANVAS.create_text(SCREEN_WIDTH+15, 15, text = "ε: %.2f%%" % (100*Flapper.epsilon), anchor = NW)
        CANVAS.create_text(SCREEN_WIDTH+150, 15, text = "α: %.3f" % (Flapper.alpha), anchor = N)
        CANVAS.create_text(SCREEN_WIDTH+300, 15, text = "Iterations: %d" % self.ITERATIONS, anchor = NE)
        CANVAS.create_text(SCREEN_WIDTH+15, 45, text = "Keyboard Shortcuts:", anchor = NW)
        CANVAS.create_text(SCREEN_WIDTH+15, 60, text = "V: Render (Disable for learning)", anchor = NW)
        CANVAS.create_text(SCREEN_WIDTH+15, 75, text = "S: Save Q-Matrix", anchor = NW)
        CANVAS.create_text(SCREEN_WIDTH+15, 90, text = "R: Restore Q-Matrix", anchor = NW)
        CANVAS.create_text(SCREEN_WIDTH+15, 105, text = "H: Human-Mode: %d (Space to switch direction)" % W.HUMAN, anchor = NW)
        CANVAS.create_text(SCREEN_WIDTH+15, 120, text = "N: Number of Birds: %d" % W.numFlap, anchor = NW)
        CANVAS.create_text(SCREEN_WIDTH+15, 135, text = "A: Rainbow Mode: %d" % W.rainbow, anchor = NW)
        CANVAS.create_text(SCREEN_WIDTH+15, 150, text = "E: Random Exploration (ε): %d" % (Flapper.epsilon != 0), anchor = NW)
        CANVAS.create_text(SCREEN_WIDTH+15, 165, text = "P: Pause", anchor = NW)
        CANVAS.create_text(SCREEN_WIDTH+15, 180, text = "Q: Exit", anchor = NW)

        
    def moveTick(self):
        self.time += 1
#    These two lines exist to verify that turning off rendering speeds things up.
#        if self.time % 100 == 0:
#            print self.time

        for item in self.flappers:
            item.moveTick()
        for item in self.flappers:
            if not item.dead:
                if not self.HUMAN:
                    if item.act(self.getLowestWall(), True):
                        item.flip()
        for item in self.walls:
            item.moveTick()
            for bird in self.flappers:
                if item.intersectsWith(bird) or bird.outOfBounds():
                    if not self.HUMAN:
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
        
def pause(event):
    W.paused = not W.paused
    
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
        if not W.rainbow:
            CANVAS.create_rectangle(self.getLeftSide(), self.getTop(), self.getRightSide(), self.getBottom(), fill="Black", width=0)
        else:
            CANVAS.create_rectangle(self.getLeftSide(), self.getTop(), self.getRightSide(), self.getBottom(), fill=random.choice(COLORS), width=0)
        
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

    #   State Space: 2*2*12*11*8*5 = 21.1k
    N_tap_div = 2
    N_acc_div = 2
    N_vel_div = 12
    N_h_div = 11
    N_v_div = 8
    N_x_div = 5
    

    tap_div = numpy.array([0, 1])
    acc_div = numpy.array([-ACCEL, ACCEL])
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
    epsilon = 0.03
    epsilon_old = epsilon
    
    #simulated annealing on learning parameters
    #After 10000 iterations, alpha goes from 0.6 to 0.5
    alpha_decay = 0.9999817680105253
    #After 1000 iterations, epsilon goes from 0.03 to 0.02
    epsilon_decay = 0.99959461708176
    
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
        new_param = ([0,1], acc_index, vel_index, h_index, v_index, x_index)
        if random.random() > self.epsilon:
            tap = self.Q[new_param].argmax()
        else:
            tap = random.choice([1, 0])
        
        #update Q matrix
        if self.old_param != []:
            reward = (SCREEN_WIDTH - abs(self.centerX - near_wall.centerX)) if life else -COST
            self.Q[self.old_param] += self.alpha * (reward + self.lam*numpy.max(self.Q[new_param]) - self.Q[self.old_param])
        
        self.old_param = (tap, acc_index, vel_index, h_index, v_index, x_index)
        self.Q_count[self.old_param] += 1
        #return action
        #0 for wait, 1 for tap (change direction of acceleration)

        return tap

    def flip(self):
        self.accel = -self.accel
        
    def outOfBounds(self):
        return not (FLAPPER_SIZE / 2 < self.centerX  < SCREEN_WIDTH - (FLAPPER_SIZE/2))

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
        self.centerY += W.DOWNWARDS_VELOCITY
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