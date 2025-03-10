# - multiplier - beto

# - user is prompted if they are ready
# - user is shown an animation of a bar rising (numbers going up)
# - if the bar exceeds a certain number (every 1.0), it resets
# - riser increases by 0.20 per second
# - enter to stop
# - if crash, 0, if save, output float @ save
# - multiplier - beto aka skrog 47
import threading
import time
from scipy.stats import gamma

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

stopped_event = threading.Event()  # Use event instead of boolean

def get_input():
    input()
    stopped_event.set()  # Signal the main thread to stop

def riser():
    input("Ready to play? (Enter)")

    stopped_event.clear()
    lower_count = 0.0
    count = 0
    sample = gamma.rvs(k, scale=theta, size=1) + 4
    bust_point = sample[0]  # Fix: Extract single value

    input_thread = threading.Thread(target=get_input)  # Remove daemon=True
    input_thread.start()

    percent = 0
    while count <= 100:
        result = lower_count + percent / 10.0

        if stopped_event.is_set():
            print("You have won!")
            print(f"multiplier: {result:.1f}")
            break

        if count >= bust_point:
            print("You have crashed!")
            print("multiplier: 0.0")
            break

        percent = min(percent, 9)  # Fix: Prevent out-of-range key access
        print(f"{lower_count}{animation[percent]}{lower_count + 1.0} Win: {result:.1f}")

        percent += 1
        count += 1

        if count % 10 == 0:
            lower_count += 1
            percent = 0

        time.sleep(0.5)

    stopped_event.set()  # Ensure the input thread can stop
    input_thread.join()  # Wait for the input thread to finish before exiting

riser()
