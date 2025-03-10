# - CSC 101 Final Project Collaborative Professor Rathi
# - Mini Casino w/ Item Shop
# - Aaron Delgado & Beto Torres 2/24/2025
class MainMenu:
    def __init__(self, coins_instance, item_instance, cheese_instance, upgrades_instance, shop_instance):
        self.coins = coins_instance
        self.items = item_instance
        self.cheese = cheese_instance
        self.upgrades = upgrades_instance
        self.shop = shop_instance

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
                game_name = input("Enter the game you want to play: ").strip()
                self.play_game(game_name)
            elif choice == "2":
                print("Your Inventory:", self.items.display_items())
            elif choice == "3":
                self.shop.display_shop()
                item_name = input("Enter item name to buy or type 'exit' to return: ").strip()
                if item_name.lower() != 'exit':
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

    def play_game(self, game_name):



    def handle_transactions(self, bet_amount, winnings):
        # Apply multipliers and update currency
        pass

    def use_item(self, item_name):
        # Handle item functionality
        pass

    def save_data(self, filename):
        # Save player data to file
        pass

    def load_data(self, filename):
        # Load player data from file
        pass

