# cheetah - beto


import time
import random


def cheetah():
    input("Press Enter to Begin...")
    print("BEWARE OF THE CHEETAH!!!")

    pause = random.randint(3000, 7000) / 1000        # determines number of seconds to wait before pouncing
    time.sleep(pause)

    print("POUNCE")
    start_time = time.time()
    input("Press Enter to Dodge.")
    reaction_time = time.time() - start_time

    result = 0.2 / (reaction_time**3)
    print(f"{reaction_time:.3f} seconds!!")
    print(f"multiplier: {result}")

cheetah()