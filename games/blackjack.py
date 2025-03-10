# - infinite blackjack/21 - beto

# - user is dealt 2 cards from a deck of cards which is sampled with replacement to allow for a random sample with duplicate cards
# - user is shown 2 brackets for the dealers cards, 1 blank
# - user is shown 2 brackets for their cards
# - user is prompted to hit or stay
# - if they hit and are above 21, instant loss
# - repeat 5&6 until user stays
# - dealer hits if they are 16 or under, stays at 17 or over
# - user beats dealer -> 2.0
# - dealer beats user -> 0.0
# - user and dealer tie -> 1.0
# - person closes to 21 wins
# - error, return error message

import random               # import random to get random numbers
from games.win_screen import win

suits = {                   # suits dictionary, defines suit strings
    0: 'Clubs',
    1: 'Diamonds',
    2: 'Hearts',
    3: 'Spades'
}

cards = {                   # card numbers dictionary, defines card strings
    0: 'Ace',
    1: '2',
    2: '3',
    3: '4',
    4: '5',
    5: '6',
    6: '7',
    7: '8',
    8: '9',
    9: '10',
    10: 'Jack',
    11: 'Queen',
    12: 'King'
}

def random_card():                                                          # function to get random card from deck
    s = suits[random.randint(0, 3)]
    c = random.randint(0, 12)
    return c, s                                                             #  returns tuple of the suit, and card value (index)

def value_card(card:int, current_total) -> int:                                        # function to determine the value of the card being added (numeric game count)
    if card == 0:                                                           # solves problem of aces being either 1 or 11 (checks value before adding)
        return 11 if current_total + 11 <= 21 else 1
    elif card >= 10:                                                        # for face cards (all valued 10)
        return 10
    else:
        return card + 1                                                     # return the numeric value of the card relative to blackjack

def hand_ui(hand) -> str:                                                   # function for displaying hand in console
    return ', '.join([f"{cards[c]} of {s}" for c, s in hand])               # returns joined string with the name of the suit and index



# blackjack game
def blackjack() -> float:
        user_hand = [random_card(), random_card()]                              # give the user/dealer a hand
        dealer_hand = [random_card(), random_card()]

        user_count = sum(value_card(card, 0) for card, _ in user_hand)                  # give the user/dealer a total numeric count for their cards
        dealer_count = sum(value_card(card, 0) for card, _ in dealer_hand)

        print("Hand dealt:", hand_ui(user_hand), "/ Total:", user_count)                            # print the user/dealer cards to show the human
        print("Dealer's hand: [Hidden],", f"{cards[dealer_hand[1][0]]} of {dealer_hand[1][1]}")

        while user_count < 21:                                                  # while the user has not yet busted; determine their move
            move = input("(hit) or (stay)? ").strip().lower()                       # move is the input to the prompt "(hit) or (stay)?"
            if move == "stay":                                               # if they stay, break
                break
            elif move == "hit":                                              # if they hit, update their count
                new_card = random_card()                                                # choose random card
                user_hand.append(new_card)                                              # append to their hand
                user_count += value_card(new_card[0], user_count)                       # calculate count
                print("Your hand:", hand_ui(user_hand), "/ Total:", user_count)         # give output in console for updated hand
                if user_count > 21:                                                     # if they bust during the hit; they lose, game over, break
                    print("Bust! You lose.")
                    break
            else:
                print("Invalid input, type (hit), (stay))")                         # error handling

        print("Dealer's hand:", hand_ui(dealer_hand), "Total:", dealer_count)       # dealers turn, show is hand again

        while dealer_count < 17:                                            # while the dealer has below 17 cards, they will hit
            new_card = random_card()                                            # get random card
            dealer_hand.append(new_card)                                        # add card to hand
            dealer_count += value_card(new_card[0], dealer_count)               # calculate count
            print("Dealer hits:", hand_ui(dealer_hand), "Total:", dealer_count) # show new dealer hand

        if user_count > 21:                                     # user loosing, user busted
            result = 0.0

        elif dealer_count > 21 or user_count > dealer_count:    # user  winning, dealer busted or user beats dealer
            win()
            result = 2.0

        elif user_count < dealer_count:                         # user loosing, dealer beats user
            print("House wins.")
            result = 0.0

        else:                                                   # push
            print("Push")
            result = 1.0
        print(f"multiplier: {result:.3f}x")
        return result                                           # return the result, 2.0/1.0/0.0


blackjack()

