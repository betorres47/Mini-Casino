# - (random) slots

# - user is shown a short animation for the wheels
# - the final roll is selected
# - if all values are the same, win! if not, loose!
# - win multiplier of 9.0 -> 1/9 chance of winning

import random
import time
from games.win_screen import win

wheel = {                                   # wheel dictionary to define characters on wheel
    0: '=====',
    1: 'seven',
    2: 'berry'
}

#add function to scale output (or number of spins) ADD HERE

def roll():                                 # roll function to print a section of animation, and define a roll
    wheels = {
        0: wheel[random.randint(0, 2)],
        1: wheel[random.randint(0, 2)],
        2: wheel[random.randint(0, 2)]
    }
    print('               |               ')
    print('=|       |+|       |-|       |=')
    print(f"=| {wheels[0]} |=| {wheels[1]} |=| {wheels[2]} |=")
    print('=|       |-|       |+|       |=')
    print('               |               ')
    return wheels

def slots():                                # slot function for the game itself,
    for x in range(0, 10):                                                         # animation
        roll()
        time.sleep(0.1)
    for x in range(0, 3):
        roll()
        time.sleep(0.33)
    for x in range(0, 2):
        roll()
        time.sleep(0.5)
    final_slots = roll()

    if final_slots[0] == final_slots[1] == final_slots[2]:                          # check if user has won
        result = 9.0
        win()
    else:
        result = 0.0                                                                # if not, user has lost
        print("You have lost.")
    print(f"multiplier: {result}")
    return result

if __name__ == "__main__":
    slots()