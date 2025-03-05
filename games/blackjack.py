# - Blackjack/21

# - deck of cards to randomly choose from, aces count as 1 if user_count + 11 > 21

# - user is dealt 2 cards from a deck of cards which is sampled with replacement to allow for a random sample with duplicate cards
# - user is shown 2 brackets for the dealers cards, 1 blank
# - user is shown 2 brackets for their cards
# - user is prompted to hit or stay
# - if they hit and are above 21, instant loss
# - repeat 5&6 until user stays
# - dealer hits if they are 16 or under, stays at 17 or over
# - user_count > dealer_count -> 2.0
# - user_count < dealer_count -> 0.0
# - user_count = dealer_count -> 1.0
# - error, return error message

import random

suits = {
    0: 'Clubs',
    1: 'Diamonds',
    2: 'Hearts',
    3: 'Spades'
}

cards = {
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

def get_card():
    s = suits[random.randint(0, 3)]
    c = random.randint(0, 12)
    return c, s

def value_card(card, current_total):
    if card == 0:  # Ace
        return 11 if current_total + 11 <= 21 else 1
    elif card >= 10:  # Face cards
        return 10
    else:
        return card + 1

def display_hand(hand):
    return ', '.join([f"{cards[c]} of {s}" for c, s in hand])

def blackjack() -> float:
    while True:
        user_hand = [get_card(), get_card()]
        dealer_hand = [get_card(), get_card()]

        user_count = sum(value_card(card, 0) for card, _ in user_hand)
        dealer_count = sum(value_card(card, 0) for card, _ in dealer_hand)

        print("Hand dealt:", display_hand(user_hand), "/ Total:", user_count)
        print("Dealer's hand: [Hidden],", f"{cards[dealer_hand[1][0]]} of {dealer_hand[1][1]}")

        while user_count < 21:
            move = input("Hit or stay? ").strip().lower()
            if move == "stay":
                break
            elif move == "hit":
                new_card = get_card()
                user_hand.append(new_card)
                user_count += value_card(new_card[0], user_count)
                print("Your hand:", display_hand(user_hand), "/ Total:", user_count)
                if user_count > 21:
                    print("Bust! You lose.")
                    break
            else:
                print("Invalid input, please type 'hit' or 'stay'.")

        print("Dealer's hand:", display_hand(dealer_hand), "Total:", dealer_count)

        while dealer_count < 17:
            new_card = get_card()
            dealer_hand.append(new_card)
            dealer_count += value_card(new_card[0], dealer_count)
            print("Dealer hits:", display_hand(dealer_hand), dealer_count)

        if user_count > 21:
            result = 0.0

        elif dealer_count > 21 or user_count > dealer_count:
            print("You have won!")
            result = 2.0

        elif user_count < dealer_count:
            print("House wins.")
            result = 0.0

        else:
            print("Push")
            result = 1.0

        print(f"multiplier: {result}")
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != "y":
            break
    return result

if __name__ == "__main__":
    blackjack()
    #function to return to menu (work in progress)