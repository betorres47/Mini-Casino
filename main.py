import currencyandstuff
from games.blackjack import blackjack
from games.cheetah import cheetah
from games.slots import slots
from games.riser import riser
from games.wof import wof
import random
import json

class MainMenu:
    def __init__(self, coins_instance, item_instance, cheese_instance, upgrades_instance, shop_instance):
        self.coins = coins_instance
        self.items = item_instance
        self.cheese = cheese_instance
        self.upgrades = upgrades_instance
        self.shop = shop_instance
        self.active_item = None  # Ensures active_item always exists

    def display_menu(self):
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
                print("Your Inventory:", self.items.display_items())
            elif choice == "3":
                self.shop.display_shop()
                item_name = input("Enter item name to buy or type 'sell' to sell an item: ").strip()

                if item_name.lower() == "sell":
                    sell_item = input("Enter the item name to sell: ").strip()
                    self.shop.selling(sell_item)
                elif item_name.lower() != 'exit':
                    quantity = int(input("Enter quantity: "))
                    self.shop.buying(item_name, quantity)
            elif choice == "4":
                print("Coins:", self.coins.display_coins())
                print("Cheese:", self.cheese.display_cheese())
            elif choice == "5":
                filename = input("Enter save file name: ").strip()
                self.save_data(filename)
            elif choice == "6":
                filename = input("Enter save file name: ").strip()
                self.load_data(filename)
            elif choice == "7":
                print("Exiting the casino. See you next time!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

    def play_game(self):
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
                return  # Return to the main menu

            if game_choice in games:
                game_name, game_function = games[game_choice]  # Get actual game name and function

                # **Allow the Player to Use an Item Before Betting**
                self.use_item()

                bet = self.get_valid_bet()  # Get a valid bet amount from the player
                winnings_multiplier = game_function()  # Run the game and get the result

                print(f"Game Result: {winnings_multiplier}x multiplier")  # Show raw game output

                # **Apply Item Effects Last**
                winnings_multiplier = self.apply_item_effects(winnings_multiplier)

                self.handle_transactions(bet, winnings_multiplier, game_name)  # Handle money transactions
                print("\n===== Updated Balances =====")
                print(f"Total Coins: {self.coins.display_coins()}")
                print(f"Total Cheese: {self.cheese.display_cheese()}")  # Show updated balance

            else:
                print("Invalid choice. Please enter a number from the list.")

    def get_valid_bet(self):
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
        """
        Handles money transactions: deducts bet, applies winnings, and updates balance.
        Ensures that item multipliers are applied last.
        """

        self.coins.remove_coins(bet_amount)  # Deduct the bet first

        if game_name == "multiplier":
            # Special case: If the Rising Multiplier crashes, the player loses everything
            if winnings_multiplier == 0:
                print("You crashed! You lost your bet!")
                return  # No winnings, no need to add anything
        elif winnings_multiplier < 1:
            print("You lost your bet!")
            return  # No need to add winnings if it's a loss
        elif winnings_multiplier == 1:
            print("It's a draw! You keep your bet.")
            self.coins.add_coins(bet_amount)  # Return the bet to player
            return

        # Step 1: Apply base winnings and upgrades
        winnings = bet_amount * winnings_multiplier * self.upgrades.winning_multiplier

        # Step 2: Apply item effects LAST
        winnings = self.apply_item_effects(winnings)

        # Add final winnings to player balance
        self.coins.add_coins(winnings)

        print(f"You won {winnings:.2f} coins!")

    def use_item(self):
        if not self.items.items:
            print("You have no items to use.")
            return

        print("\n===== Your Items =====")
        for item, qty in self.items.items.items():
            print(f"{item} (x{qty})")

        item_choice = input("Enter the item name to use (or type 'none' to skip): ").strip().lower()

        if item_choice in self.items.items and self.items.items[item_choice] > 0:
            print(f"Using {item_choice}...")
            self.items.remove_item(item_choice)  # Remove item from inventory
            self.active_item = item_choice  # Store the active item for the game
        else:
            print("Invalid choice or no such item available.")
            self.active_item = None  # No active item

    def apply_item_effects(self, winnings):
        if self.active_item:
            if self.active_item == "Prize Doubler":
                winnings *= 2  # Double the winnings
                print("Prize Doubler applied! Winnings doubled.")
            elif self.active_item == "Random Prize Multiplier":
                random_multiplier = random.uniform(0.5, 3.0)  # Multiplier between 0.5x and 3.0x
                winnings *= random_multiplier
                print(f"Random Prize Multiplier applied! Winnings multiplied by {random_multiplier:.2f}x.")

        # Ensure the item effect is cleared after use
        self.active_item = None
        return winnings

    def save_data(self, filename="save_file.json"):
        """
        Saves player data to a valid JSON file.
        """
        data = {
            "coins": self.coins.display_coins(),
            "items": self.items.display_items() if self.items.items else {},
            "cheese": self.cheese.display_cheese(),
            "winning_multiplier": self.upgrades.winning_multiplier,
            "purchase_multiplier": self.upgrades.purchase_multiplier
        }

        json_string = json.dumps(data, indent=4)  # Convert data to a JSON string first

        with open(filename, "w", encoding="utf-8") as file:  # Open file in write mode
            file.write(json_string)  # Write JSON string manually

        print(f"Game saved to {filename}!")

    def load_data(self, filename="save_file.json"):
        """
        Loads player data from a JSON file.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                json_string = file.read()  # Read entire file as a string
                data = json.loads(json_string)  # Convert string back to JSON object

            self.coins.coins = data["coins"]
            self.items.items = data["items"]
            self.cheese.cheese_slices = data["cheese"]["Cheese Slices"]
            self.cheese.cheese_flakes = data["cheese"]["Cheese Flakes"]
            self.upgrades.winning_multiplier = data["winning_multiplier"]
            self.upgrades.purchase_multiplier = data["purchase_multiplier"]

            print(f"Game loaded from {filename}!")
        except FileNotFoundError:
            print(f"No save file found! Starting a new game.")
        except json.JSONDecodeError:
            print(f"Error loading save file! Data may be corrupted.")


if __name__ == "__main__":
    coins = currencyandstuff.Coins()
    items = currencyandstuff.Item()
    cheese = currencyandstuff.Cheese()
    upgrades = currencyandstuff.Upgrades()
    shop = currencyandstuff.Shop(coins, items, cheese, upgrades)

    currencyandstuff.load_data(coins, items, cheese)
    main = MainMenu(coins, items, cheese, upgrades, shop)
    main.display_menu()