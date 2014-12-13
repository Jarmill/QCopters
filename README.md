QCopters
========

Reinforcement (Q) learning agent that learns to play SwingCopters. Final Project for AI (NU 4100)
Swing Copters is the second popular and frustrating game created by Nguyễn Hà Đông (Dong Nguyen), on the heels of the wildly successful Flappy Bird. In Swing Copters, players control a tiny helicopter which moving upwards at a constant rate, and moving while constantly accelerating to either the left or right. Tapping the screen toggles the direction of the helicopter’s acceleration between left and right, but leaves the magnitude unchanged. The helicopter must pass through gaps and dodge swinging hammers. As a result, the helicopter has a somewhat parabolic path, as superimposed in red on the screenshot below. The game is scored based on the number of gaps successfully passed through. 

We re-implemented a simplified version of Swing Copters, with no hanging hammers, but with the accelerative physics largely unchanged, and similar scoring. Then, we wrote a Reinforcement Learning agent to learn to play our representation of Swing Copters. To play the game manually, press the “H” key on the keyboard to switch into Human Mode, in which you can toggle the direction with the spacebar. In Human Mode, no learning data is stored, since Q learning is unsupervised.

All work was done in Python 2.7.x. We used Tkinter as a front end to display the game. No logic or collision detection was done in Tkinter, so  we were able to turn off rendering in order to increase the speed for learning. This is accessible by pressing “V” on the keyboard. Numpy was used to facilitate multidimensional array computation and storage of the Q matrix.

Run main.py to start the program. Numpy is required, and this program was intended for use in Python 2.7
