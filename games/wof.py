# - wheel of fortune (wof) - beto

# - user is shown a short animation of a wheel and a list of prizes (the wheel goes though the animation in order)
# - the final prize is selected
# - prize is revealed (TBD implemented w/ shop maybe)
# - play again? y/n

import random
import time
from games.win_screen import win

wheel = {}                                                  # define wheel of prizes
for x in range(6):
    wheel[x] = 0.0
for x in range(5, 11):
    wheel[x] = 1.0
for x in range(10, 16):
    wheel[x] = 2.0
for x in range(15, 20):
    wheel[x] = 3.0
wheel[20] = 5.0

#add function to scale output (or number of spins) ADD HERE

def spin(x):                                        # roll function to print a section of animation, and define a roll
    print(f"--0{wheel[x]}0--")
    print('0   |   0')
    print(' 0  +  0  ')
    print(' 0  +  0 ')
    print('0   |   0')
    return wheel[x]

def wof():                                                                            # wheel of fortune game
        counter = random.randint(0, 20)                                         #start wheel at a random point
        for x in range(50):                                                           # animation, 50 'ticks' each 0.05s apart
            spin(counter)
            counter += 1
            if counter > 20:
                counter = 0
            time.sleep(0.05)
        result = wheel[counter]                                       # show the result
        if result != 0:                                                       # user wins
            win()
        else:                                                                         # user looses
            print("You have lost.")
        print(f"multiplier: {result:.3f}x")
        return result


wof()
