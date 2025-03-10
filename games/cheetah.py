import time
import random
from os import waitpid


def reaction_time_game():
    input("Are you ready? Press Enter to start...")

    wait_time = random.randint(1000, 5000) / 1000  # Convert to seconds
    time.sleep(wait_time)

    print("CLICK!")
    start_time = time.time()
    input("Press Enter as fast as you can!")
    reaction_time = time.time() - start_time

    print(f"Your reaction time: {reaction_time:.3f} seconds")


if __name__ == "__main__":
    reaction_time_game()

def cheetah():
    input("Press Enter to Begin...")
    print("BEWARE OF THE CHEETAH!!!")

    pause = random.randint(1000, 50000) / 1000        # determines number of seconds to wait before pouncing
    time.sleep(pause)

    print("POUNCE")