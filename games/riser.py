# - riser

# - user is prompted if they are ready
# - user is shown an animation of a bar rising (numbers going up)
# - if the bar exceeds a certain number (every 1.0), it resets
# - riser increases by 0.20 per second
# - enter to stop
# - if crash, 0, if save, output float @ save

import threading
import time
from scipy.stats import gamma                   # library to create statistical distributions
from games.win_screen import win

k = 0.167
theta = 102                                     # parameters for winning distribution

animation = {                                   # dictionary of animations
    0: "[##########]",
    1: "[#---------]",
    2: "[##--------]",
    3: "[###-------]",
    4: "[####------]",
    5: "[#####-----]",
    6: "[######----]",
    7: "[#######---]",
    8: "[########--]",
    9: "[#########-]"
}

stopped_event = threading.Event()                       # use event (problems with boolean)

def get_input():                                        # set up input threading function to monitor for user input
    input()
    stopped_event.set()                                 # signal the main thread to stop

def riser():
    input("Ready to play? (Enter)")

    stopped_event.clear()                               # ensure input is cleared, counts are at zero defined outside loops
    lower_count = 0.0
    count = 0
    sample = gamma.rvs(k, scale=theta, size=1) + 4      # sample a random value from statistical distribution totally not meant to favor the house
    bust_point = sample[0]                              # set the breaking point to the sample

    input_thread = threading.Thread(target=get_input)   #monitor for input (begin threaded function)
    input_thread.start()

    percent = 0                                         # define result and percent outside loops
    result = 0.0

    while count <= 100:                                 # begin rise
        result = count / 10.0

        if stopped_event.is_set():                      # if they stop before the break, player wins
            win()
            break



        if count >= bust_point:                         # player looses
            result = 0.0
            print("You have crashed!")
            break


        percent = min(percent, 9)                       # prevent out of range error w/ percent
        print(f"{lower_count}{animation[percent]}{lower_count + 1.0} Win: {result:.1f}") # loading bar

        percent += 1
        count += 1                                      # rise count and percent

        if count % 10 == 0:                             # reset loading bar
            lower_count += 1
            percent = 0


        time.sleep(0.5)                                 # pause to wait for input, stability


    stopped_event.set()
    input_thread.join()                                 # get input threat to stop and join to prevent errors

    print(f"multiplier: {result:.3f}x")                 # show winnings
    return result

if __name__ == "__main__":
    riser()





