"""

   ▄▄▄▄███▄▄▄▄    ▄█  ███▄▄▄▄    ▄█        ▄████████    ▄████████    ▄████████  ▄█  ███▄▄▄▄    ▄██████▄     █▄
 ▄██▀▀▀███▀▀▀██▄ ███  ███▀▀▀██▄ ███       ███    ███   ███    ███   ███    ███ ███  ███▀▀▀██▄ ███    ███    ███
 ███   ███   ███ ███▌ ███   ███ ███▌      ███    █▀    ███    ███   ███    █▀  ███▌ ███   ███ ███    ███    ███
 ███   ███   ███ ███▌ ███   ███ ███▌      ███          ███    ███   ███        ███▌ ███   ███ ███    ███    ███
 ███   ███   ███ ███▌ ███   ███ ███▌      ███        ▀███████████ ▀███████████ ███▌ ███   ███ ███    ███    ███
 ███   ███   ███ ███  ███   ███ ███       ███    █▄    ███    ███          ███ ███  ███   ███ ███    ███     ██
 ███   ███   ███ ███  ███   ███ ███       ███    ███   ███    ███    ▄█    ███ ███  ███   ███ ███    ███      ▀
  ▀█   ███   █▀  █▀    ▀█   █▀  █▀        ████████▀    ███    █▀   ▄████████▀  █▀    ▀█   █▀   ▀██████▀      █▀

                                                                                created by Aaron Delgado and Beto Torres
                                                                                    version 1.0 alpha - 3/10/2025
                                                                                                                     """

import currencyandstuff                             # import all required libraries
from games.blackjack import blackjack
from games.cheetah import cheetah
from games.slots import slots
from games.riser import riser
from games.wof import wof
import random

#MainMenu class handles menu for the casino
class MainMenu:
    def __init__(self, coins_instance, item_instance, cheese_instance, upgrades_instance, shop_instance):
        self.coins = coins_instance
        self.items = item_instance
        self.cheese = cheese_instance
        self.upgrades = upgrades_instance
        self.shop = shop_instance
        self.active_item = None #Stores the item that is in use

    def display_menu(self):
        #Displays and handles the choices the player makes
        while True:
            print("\n===== Mini Casino Menu =====")
            print("1. Play a Game")
            print("2. View Inventory")
            print("3. Visit Shop")
            print("4. View Cheese & Coins")
            print("5. Save Game")
            print("6. Load Game")
            print("7. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.play_game()
            elif choice == "2":
                self.display_inventory()
            elif choice == "3":
                self.shop.display_shop()
            elif choice == "4":
                print("Coins:", self.coins.display_coins())
                print("Cheese:", self.cheese.display_cheese())
            elif choice == "5":
                self.save_data("save")
            elif choice == "6":
                self.load_data("save")
            elif choice == "7":
                print("Exiting the casino. See you next time!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

    def display_inventory(self):
        #Displays everything the play has
        print("\n===== Inventory =====")

        # Display regular items
        if self.items.items:
            print("Items:")
            for item, qty in self.items.items.items():
                print(f"- {item} (x{qty})")
        else:
            print("No items in inventory.")

        # Display multipliers separately
        print("\nMultipliers:")
        print(f"- Winning Multiplier: {self.upgrades.winning_multiplier:.2f}x")
        print(f"- Purchase Multiplier: {self.upgrades.purchase_multiplier:.2f}x")

    def play_game(self):
        #Handles what game is chosen and how its executed
        games = {
            "1": ("blackjack", blackjack),
            "2": ("slots", slots),
            "3": ("wof", wof),
            "4": ("multiplier", riser),
            "5": ("cheetah", cheetah)
        }

        while True:
            print("\n===== Available Games =====")
            for num, (name, _) in games.items():
                print(f"{num}. {name}")

            print("0. Back to Main Menu")

            game_choice = input("\nEnter the number of the game you want to play: ").strip()

            if game_choice == "0":
                return

            if game_choice in games:
                game_name, game_function = games[game_choice]

                self.use_item()

                bet = self.get_valid_bet()
                winnings_multiplier = game_function()

                print(f"Game Result: {winnings_multiplier}x multiplier")

                winnings_multiplier = self.apply_item_effects(winnings_multiplier)

                self.handle_transactions(bet, winnings_multiplier, game_name)
                print("\n===== Updated Balances =====")
                print(f"Total Coins: {self.coins.display_coins()}")
                print(f"Total Cheese: {self.cheese.display_cheese()}")

            else:
                print("Invalid choice. Please enter a number from the list.")

    def get_valid_bet(self):
        #Makes sure the player puts a valid bet
        while True:
            try:
                bet = float(input("Enter your bet amount: "))
                if bet <= 0:
                    print("Bet must be greater than zero.")
                elif bet > self.coins.display_coins():
                    print("You do not have enough coins for this bet.")
                else:
                    return bet
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    def handle_transactions(self, bet_amount, winnings_multiplier, game_name):
        #Handles how much a play wins or loses
        self.coins.remove_coins(bet_amount)

        if game_name == "multiplier":
            if winnings_multiplier == 0:
                print("You crashed! You lost your bet!")
                return
        elif winnings_multiplier < 1:
            print("You lost your bet!")
            return
        elif winnings_multiplier == 1:
            print("It's a draw! You keep your bet.")
            self.coins.add_coins(bet_amount)
            return

        winnings = bet_amount * winnings_multiplier * self.upgrades.winning_multiplier
        winnings = self.apply_item_effects(winnings)
        self.coins.add_coins(winnings)

        print(f"You won {winnings:.2f} coins!")

    def use_item(self):
        #Handles if a user uses an item or not
        #Prompted before betting amount
        if not self.items.items:
            print("You have no items to use.")
            return

        print("\n===== Your Items =====")
        for item, qty in self.items.items.items():
            print(f"- {item} (x{qty})")

        while True:
            item_choice = input("Enter the item name to use (or type 'none' to skip): ").strip()

            if item_choice.lower() == "none":
                self.active_item = None
                print("No item selected.")
                return

            # Ensure the selected item is valid
            if item_choice in self.items.items and self.items.items[item_choice] > 0:
                print(f"Using {item_choice}...")
                self.items.remove_item(item_choice)  #Remove used item from inventory
                self.active_item = item_choice  #Store item to apply effects
                return
            else:
                print("Invalid choice or no such item available. Please enter a valid item name.")

    def apply_item_effects(self, winnings):
        #Handles the affect of each item
        if self.active_item:
            if self.active_item == "Prize Doubler":
                winnings *= 2
                print("Prize Doubler applied! Winnings doubled.")
            elif self.active_item == "Random Prize Multiplier":
                random_multiplier = random.uniform(0.5, 3.0)
                winnings *= random_multiplier
                print(f"Random Prize Multiplier applied! Winnings multiplied by {random_multiplier:.2f}x.")

        self.active_item = None #ensures that the item affect doesn't carry over and resets
        return winnings

    def save_data(self, filename="save"):
        #Takes data stored in the code and edits the file accordingly
        #Does full replacement of the code for it to be easier
        #If there is an error it will display error code for the user to try and debug
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Coins: {self.coins.display_coins()}\n")
                file.write(f"Items: {self.items.display_items()}\n")
                file.write(f"Cheese Slices: {self.cheese.cheese_slices}\n")
                file.write(f"Winning Multiplier: {self.upgrades.winning_multiplier}\n")
                file.write(f"Purchase Multiplier: {self.upgrades.purchase_multiplier}\n")
                file.write(f"Multiplier Prices:\n")
                file.write(f"  Prize Multiplier Upgrade: {self.shop.shop_inventory['Prize Multiplier Upgrade']}\n")
                file.write(
                    f"  Purchase Multiplier Upgrade: {self.shop.shop_inventory['Purchase Multiplier Upgrade']}\n")

            print(f"Game saved to {filename}!")
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_data(self, filename="save"):
        #Uploads the data from the file to the game.
        #This is the first function ran
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()

            current_section = None  # Track when reading multi-line sections

            for line in lines:
                line = line.strip()
                if not line or line.startswith("Multiplier Prices"):
                    current_section = "multipliers"  # Mark that we are reading multipliers next
                    continue  # Skip header lines

                if current_section == "multipliers":
                    # Read each multiplier price line safely
                    parts = line.split(": ", 1)
                    if len(parts) == 2:
                        key, value = parts
                        if key.strip() == "Prize Multiplier Upgrade":
                            self.shop.shop_inventory["Prize Multiplier Upgrade"] = int(value)
                        elif key.strip() == "Purchase Multiplier Upgrade":
                            self.shop.shop_inventory["Purchase Multiplier Upgrade"] = int(value)
                    continue  # Move to next line

                # Read normal key-value pairs
                parts = line.split(": ", 1)
                if len(parts) == 2:
                    key, value = parts
                    key = key.strip()
                    value = value.strip()

                    if key == "Coins":
                        self.coins.coins = int(value)
                    elif key == "Items":
                        self.items.items = eval(value) if value != "{}" else {}
                    elif key == "Cheese Slices":
                        self.cheese.cheese_slices = int(value)
                    elif key == "Winning Multiplier":
                        self.upgrades.winning_multiplier = float(value)
                    elif key == "Purchase Multiplier":
                        self.upgrades.purchase_multiplier = float(value)
            #This will prompt if ran successfully
            print(f"Game loaded from {filename}!")
        except FileNotFoundError:
            #This will prompt if the file is not found and will start
            print("No save file found! Starting a new game.")
        except Exception as e:
            #This will prompt if different error occurs
            print(f"Error loading save file: {e}")


if __name__ == "__main__":
    coins = currencyandstuff.Coins()
    items = currencyandstuff.Item()
    cheese = currencyandstuff.Cheese()
    upgrades = currencyandstuff.Upgrades()
    shop = currencyandstuff.Shop(coins, items, cheese, upgrades)

    main = MainMenu(coins, items, cheese, upgrades, shop)
    main.load_data("save")
    main.display_menu()
