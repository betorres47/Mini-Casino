# cheetah - beto


import time
import random
from games.win_screen import win


def cheetah():
    input("Press Enter to Begin...")
    print("BEWARE OF THE CHEETAH!!! (press Enter to dodge!")

    pause = random.randint(3000, 7000) / 1000        # determines number of seconds to wait before pouncing
    time.sleep(pause)

    print("POUNCE")
    start_time = time.time()
    input("Dodge!")
    reaction_time = time.time() - start_time

    result = 0.2 / (reaction_time**3)

    if result >= 1:
        win()
        print(f"multiplier: {result:.3f}x")
    else:
        result = 0.0
        print("You have been mauled.")
        print(f"multiplier: {result:.3f}x")

    print(f"You reacted in {reaction_time:.3f}s")
    return result

cheetah()