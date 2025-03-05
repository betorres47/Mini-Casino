# - wheel of fortune (wof) - beto aka skrog 47

# - user is shown a short animation of a wheel and a list of prizes (the wheel goes though the animation in order)
# - the final prize is selected
# - prize is revealed (TBD implemented w/ shop maybe)
# - play again? y/n

import random
import time

wheel = {}                                                  # define wheel of prizes
for x in range(6):
    wheel[x] = 0.0
for x in range(5, 11):
    wheel[x] = 1.0
for x in range(10, 16):
    wheel[x] = 2.0
for x in range(15, 20):
    wheel[x] = 3.0
wheel[20] = 5.0

#add function to scale output (or number of spins) ADD HERE

def spin(x):                                        # roll function to print a section of animation, and define a roll
    print(f"--0{wheel[x]}0--")
    print('0   |   0')
    print(' 0  +  0 ')
    print(' 0  +  0 ')
    print('0   |   0')
    return wheel[x]

def wof():                                                                            # wheel of fortune game
    while True:
        counter = random.randint(0, 20)                                         #start wheel at a random point
        for x in range(50):                                                           # animation, 50 'ticks' each 0.05s apart
            spin(counter)
            counter += 1
            if counter > 20:
                counter = 0
            time.sleep(0.05)
        print(f"multiplier: {wheel[counter]}")                                        # show the result
        if wheel[counter] != 0:                                                       # user wins
            print("You have won!")
        else:                                                                         # user looses
            print("You have lost.")

        play_again = input("Play again? (yes): ").strip().lower()                       #function to return to menu (work in progress) FIX THE FREAKING PLAY AGAIN FOR ALL GAMES!!
        if play_again != "yes":
            break
        else:
            print("Invalid input, type (yes)")
    return wheel[counter]

if __name__ == "__main__":
    wof()
