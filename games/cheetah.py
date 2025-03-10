# cheetah

# reaction based game
# player will  be prompted when they are ready
# the cheetah will pounce on the player
# if the player reacts fast enough they manage to escape
# if not they get mauled.

import time
import random
from idlelib.debugger_r import restart_subprocess_debugger

from games.win_screen import win

def cheetah():
    input("Press Enter to Begin...")                                        # start the game when the player presses Enter
    print("BEWARE OF THE CHEETAH!!! (press Enter to dodge!)")

    pause = random.randint(3000, 7000) / 1000                         # random delay between 3 and 7 seconds
    time.sleep(pause)


    print("POUNCE")                                                         # cheetah pounces after the wait is over
    reaction_time = 0
    start_time = time.time()                                                # start timing the player's reaction
    if input("Dodge!") == "":                                               # player tries to dodge after pounce
        reaction_time = time.time() - start_time                            # reaction time

    if reaction_time <= 0.01:                                                  # incase subhuman reaction time or early input
        result = 0.0
        print("Too early! The cheetah caught you.")
        print(f"multiplier: {result}")
        return result


    result = 0.2 / (reaction_time ** 3)                                     # calculate result using totally not house favored odds (again)


    if result >= 1:                                                         # played escaped
        win()
        print(f"multiplier: {result:.3f}x")
    else:                                                                   # player gets mauled
        result = 0.0
        print("You have been mauled.")
        print(f"multiplier: {result:.3f}x")

    print(f"You reacted in {reaction_time:.3f}s")                           # display the reaction time
    return result                                                           # result


if __name__ == "__main__":
    cheetah()
