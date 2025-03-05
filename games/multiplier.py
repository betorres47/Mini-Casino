# - multiplier - beto aka skrog 47

# - user is prompted if they are ready
# - user is shown an animation of a bar rising (numbers going up)
# - if the bar exceeds a certain number (every 1.0), it resets
# - riser increases by 0.20 per second
# - enter to stop
# - if crash, 0, if save, float @ save
import random
import time
import threading
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma

k = 0.167                         # shape parameters for stats
theta = 102


animation = {                   # animation frames
    0: "[----------]",
    1: "[#---------]",
    2: "[##--------]",
    3: "[###-------]",
    4: "[####------]",
    5: "[#####-----]",
    6: "[######----]",
    7: "[#######---]",
    8: "[########--]",
    9: "[#########-]",
    10: "[##########]",
}

stopped = False                 # user input default false

def get_input():                # monitor for user input using global threat stopped
    global stopped
    input()
    stopped = True              # set stopped to true if input is detected



def riser():                                            # riser game
    while True:
        input("Are you ready? (Enter)")                 # are you ready?

        global stopped                                  # threading
        stopped = False                                 # reset variables
        lower_count = 0.0
        count:float = 0.0
        bust_point = gamma.rvs(k, scale=theta, size=1)  # random crash point using gamma plot
        percent = 0

        input_thread = threading.Thread(target=get_input, daemon=True)          # detect for input
        input_thread.start()

        for x in range(0, 101):                         # for loop to get loading bar and counter
            if stopped:                                 # if user decides to stop print results
                result = count / 10
                print("You have won!")
                print(f"multiplier: {count / 10}")
                break

            if count >= bust_point:                     # user busts
                print("You have crashed!")
                print("multiplier: 0.0")
                break

            if (count % 10) == 0:                       # add to count and lower_count when needed
                lower_count += 1
                percent = 0
                print(f"{lower_count}{animation[0]}{lower_count + 1.0} Win: {count / 10}")
            else:
                print(f"{lower_count}{animation[percent]}{lower_count + 1.0} Win: {count / 10}")
            percent += 1
            count += 1
            time.sleep(0.5)

# ADD PLAY AGAIN

if __name__ == "__main__":
    riser()