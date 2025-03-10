# - riser - beto

# - user is prompted if they are ready
# - user is shown an animation of a bar rising (numbers going up)
# - if the bar exceeds a certain number (every 1.0), it resets
# - riser increases by 0.20 per second
# - enter to stop
# - if crash, 0, if save, output float @ save

import threading
import time
from scipy.stats import gamma
from games.win_screen import win

k = 0.167
theta = 102

animation = {
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

stopped_event = threading.Event()               # use event (problems with boolean)

def get_input():
    input()
    stopped_event.set()                         # signal the main thread to stop

def riser():
    input("Ready to play? (Enter)")

    stopped_event.clear()
    lower_count = 0.0
    count = 0
    sample = gamma.rvs(k, scale=theta, size=1) + 4
    bust_point = sample[0]

    input_thread = threading.Thread(target=get_input)
    input_thread.start()

    percent = 0
    result = 0.0

    while count <= 100:
        result = count / 10.0

        if stopped_event.is_set():
            win()
            break



        if count >= bust_point:
            result = 0.0
            print("You have crashed!")
            break


        percent = min(percent, 9)                  # prevent out of range error
        print(f"{lower_count}{animation[percent]}{lower_count + 1.0} Win: {result:.1f}")

        percent += 1
        count += 1

        if count % 10 == 0:
            lower_count += 1
            percent = 0


        time.sleep(0.5)


    stopped_event.set()
    input_thread.join()                             # get input threat to stop and join to prevent errors

    print(f"multiplier: {result:.3f}x")
    return result

riser()



