QCopters
========

Reinforcement (Q) learning agent that learns to play SwingCopters. Final Project for AI (NU 4100)

There are three parts to this project, the game display, game programming, and AI learning.

Game Display:
Pygame will be used as a framework to develop and program SwingCopters.
Humans should be able to input and play SwingCopters, and as such, we will be rewriting and cloning the game.
Bindings will also be provided in order for the AI agent to play without requiring the display.

Game Programming:
This entire project will use an object-oriented approach in order for objects to interact and behave properly.
The programming section provides the physics of the game and keeping track of all relevant parameters

AI learning:
Every time step, the agent has a chance to perform an action (change direction of acceleration, henceforth referred to as "tap") or not
Once the agent decides whether to tap or not, physics calculations are conducted and a new state is presented to the agent.
Tapping instantaneously flips the sign of the acceleration, which only affects ax, since ay = 0.
The tiebreaker is to not tap and do nothing, since that is the more common action.
There is still a delay before the velocity changes, which the agent must be aware of.

Reinforcement learning (Q learning) will be used to train the agent.

The agent state (observable) is a subset of the game state.
Agent state (5 fields) 
    Vertical distance to next gate: 20
    Horizontal distance to wall: 40
        possibly a horizontal distance to middle of gap?
        Or maybe horizontal distance to pair of pipes (0 if inside range of pipes, negative if left or positive if right)
    Current horizontal velocity: 15 (This # should maybe depend on physics dt?)
    Direction of horizontal acceleration: 2
    Angle of hammers (?): 200
    State space = 20*40*15*2*30 = 480k conservatively, can be reduced
    
Life (whether agent is living) does not have to be a state, instead it can be incorporated into the reward function.
    
The world state includes more parameters such as:
    Gate positions (vertical spacing, horizontal gap size and positioning)
    Angle of all hammers
    Score (number of successful gates passed)
    
The reward function is:
    +1 / time step while still alive (instantaneous)
    -1000 for dying
    Max iteration (survive 100 gates) rewards will not be given, since that would poison/skew the Q table.

Other Q learning parameters:
    discount factor lambda = 1
    alpha = 0.7-0.8
    might also add random chance to accelerate learning, might backfire though.

Q learning is known for being very slow, and might take hours of computing time and power.
We might try to simulate multiple agents at once iteratively,
or have multiple cores communicating and solving the problem independently (multiprocessing module in Python).
Communication/waiting overhead might be an issue.   
    
We might start by implementing flappy bird, which is simpler than SwingCopters.
    
Dependancies:
    Pygame
    Numpy (?)
