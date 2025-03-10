# cheetah

# reaction based game
# player will  be prompted when they are ready
# the cheetah will pounce on the player
# if the player reacts fast enough they manage to escape
# if not they get mauled.


import time
import random
from games.win_screen import win


def cheetah():
    input("Press Enter to Begin...")
    print("BEWARE OF THE CHEETAH!!! (press Enter to dodge!)")      # begins reaction test

    pause = random.randint(3000, 7000) / 1000               # determines number of seconds to wait before pouncing
    time.sleep(pause)

    print("POUNCE")                                               # displays cheetah
    start_time = time.time()                                      # begins timer to determine reaction time
    input("Dodge!")
    reaction_time = time.time() - start_time

    result = 0.2 / (reaction_time**3)                             # calculate reaction time and result from reaction time

    if result >= 1:                                               # player did not escape...
        win()
        print(f"multiplier: {result:.3f}x")
    else:                                                         # player escaped
        result = 0.0
        print("You have been mauled.")
        print(f"multiplier: {result:.3f}x")

    print(f"You reacted in {reaction_time:.3f}s")                 # display reaction time
    return result

