# Pseudocode for Swing Copters
# Still missing: exact details of where we actually do the Q-Learning
# Translation into actual python ongoing
import pygame

def main(argv=None):
    if argv is None:
        argv = sys.argv
    #set the boolean variable RENDER, which has been passed in
    #set the parameters for various configuration things
    #make a screen
    #run loop: (could maybe be broken into its own function)
        #process input
        #update locations of sprites; also their fields
            #if things go off the bottom of the screen, we make new ones higher up.
            #check for loss
        #update weights
        #render, if RENDER
    
class sprite():
    #rect = pygamerectangle
    def intersectsWith(a_sprite):
        #return true or false
    
class flapper(sprite):
    #all the aspects of our item

class hammer(sprite):
    #plus direction swinging
    #and angle if we have time for that and can figure out how to do it nicely in pygame

if __name__ == "__main__":
    main()