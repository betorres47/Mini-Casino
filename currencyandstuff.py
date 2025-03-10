

# Class to handle inventory items
class Item:
    def __init__(self):  # Initializes inventory
        self.items = {}

    def add_items(self, item_name, quantity):  # Adds items to inventory
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity

    def remove_item(self, item_name):  # Removes an item from inventory
        if item_name in self.items and self.items[item_name] > 0:
            self.items[item_name] -= 1
            if self.items[item_name] == 0:  # Deletes item if quantity is 0
                del self.items[item_name]
        else:
            print(f"Item {item_name} was not found")

    def display_items(self):  # Displays all items in inventory
        return self.items


# Class to manage cheese-related currency
class Cheese:
    def __init__(self):
        self.cheese_slices = 0  # Represents the player's cheese slices

    def add_cheese(self, amount):  # Adds cheese slices
        self.cheese_slices += amount

    def remove_cheese(self, amount):  # Removes cheese slices (if enough available)
        if self.cheese_slices >= amount:
            self.cheese_slices -= amount
        else:
            print("Not enough cheese slices")

    def display_cheese(self):  # Displays the number of cheese slices
        return {"Cheese Slices": self.cheese_slices}


# Class to manage player coins
class Coins:
    def __init__(self, total_coins=200):  # Starts player with default 200 coins
        self.coins = round(total_coins)  # Ensures starting balance is rounded

    def add_coins(self, amount):  # Adds coins to the player's balance
        self.coins += amount
        self.coins = round(self.coins)  # Ensures coins remain whole numbers

    def remove_coins(self, amount):  # Deducts coins from balance if enough available
        if self.coins >= amount:
            self.coins -= amount
            self.coins = round(self.coins)  # Ensures coins are rounded
        else:
            print("You don't have enough coins to buy!")

    def display_coins(self):  # Displays current coin balance
        return self.coins


# Shop class manages buying and selling items
class Shop:
    def __init__(self, coins_instance, item_instance, cheese_instance, upgrades_instances):
        self.coins_instance = coins_instance  # Connects to player’s coins
        self.item_instance = item_instance  # Connects to inventory
        self.cheese_instance = cheese_instance  # Connects to cheese currency
        self.upgrades_instances = upgrades_instances  # Connects to upgrades

        # Standard items for sale in the shop
        self.shop_inventory = {
            "Prize Multiplier Upgrade": 10000,
            "Purchase Multiplier Upgrade": 10000,
            "Cheese Wheel": 2000,
            "Huge Cheese Wheel": 15000,
            "Prize Doubler": 10000,
            "Random Prize Multiplier": 1000,
        }
        # Special items (purchased with cheese slices)
        self.special_items = {
            "Super Cool Trophy": 100000000
        }

    def display_shop(self):  # Displays the shop and available items
        print("\n===== Shop Inventory =====")
        print(f"Total Coins: {self.coins_instance.display_coins()} coins")
        print(f"Total Cheese Slices: {self.cheese_instance.cheese_slices}")

        # Display standard items
        for index, (item, price) in enumerate(self.shop_inventory.items(), start=1):
            print(f"{index}. {item} - {price} coins")

        # Display special items (purchased with cheese)
        print("\n===== Special Items (Cheese Slices Only) =====")
        for index, (item, price) in enumerate(self.special_items.items(), start=len(self.shop_inventory) + 1):
            print(f"{index}. {item} - {price} cheese slices")

        while True:
            item_choice = input("Enter item name to buy, type 'sell' to sell, or 'exit' to leave: ").strip()

            if item_choice.lower() == "exit":
                break  # Exits the shop menu
            elif item_choice.lower() == "sell":
                sell_item = input("Enter the item name to sell: ").strip()
                self.selling(sell_item)  # Calls the selling function
            elif item_choice in self.shop_inventory or item_choice in self.special_items:
                self.buying(item_choice)  # Calls the buying function
            else:
                print("Invalid item name! Please enter a valid item from the shop.")

    def buying(self, item_name):
        #Handles purchasing items
        try:
            if item_name in self.special_items:
                # Special items (Super Cool Trophy) use cheese slices instead of coins
                if self.cheese_instance.cheese_slices >= self.special_items[item_name]:
                    self.cheese_instance.remove_cheese(self.special_items[item_name])
                    self.item_instance.add_items(item_name, 1)
                    print(f"Successfully purchased {item_name}!")
                    print(f"Remaining Cheese Slices: {self.cheese_instance.cheese_slices}")
                else:
                    print("You don't have enough cheese slices!")
                return

            if item_name in self.shop_inventory:
                # If the item is a multiplier, auto-set quantity to 1
                if item_name in ["Prize Multiplier Upgrade", "Purchase Multiplier Upgrade"]:
                    quantity = 1
                    print(f"Multipliers can only be bought one at a time. Quantity set to 1.")
                else:
                    # Ask for quantity for normal items
                    quantity = input("Enter quantity: ").strip()
                    if not quantity.isdigit() or int(quantity) < 1:
                        print("Invalid quantity. Please enter a valid number (1 or more).")
                        return
                    quantity = int(quantity)

                # Calculate price with discount
                base_price = self.shop_inventory[item_name] * quantity
                final_price = base_price * self.upgrades_instances.purchase_multiplier

                # Check if the player has enough coins
                if self.coins_instance.coins >= final_price:
                    self.coins_instance.remove_coins(final_price)

                    # Apply effects directly for multipliers
                    if item_name == "Prize Multiplier Upgrade":
                        self.upgrades_instances.add_winning_multiplier()
                        self.shop_inventory[item_name] = int(self.shop_inventory[item_name] * 1.5)
                    elif item_name == "Purchase Multiplier Upgrade":
                        self.upgrades_instances.add_purchase_multiplier()
                        self.shop_inventory[item_name] = int(self.shop_inventory[item_name] * 1.5)
                    else:
                        self.item_instance.add_items(item_name, quantity)

                    print(f"Successfully purchased {quantity} {item_name}(s) for {final_price:.2f} coins!")
                    print(f"Remaining Coins: {self.coins_instance.display_coins()}")
                else:
                    print("You don't have enough coins!")

        except ValueError:
            print("Invalid input. Please enter a valid number for quantity.")

    def selling(self, item_name):
        #Handles selling items back to the shop while preventing upgrades from being sold.
        if item_name in ["Prize Multiplier Upgrade", "Purchase Multiplier Upgrade"]:
            print("You cannot sell upgrades!")  #Prevents selling upgrades
            return

        if item_name in self.item_instance.items and self.item_instance.items[item_name] > 0:
            if item_name in self.shop_inventory:
                sell_price = self.shop_inventory[item_name] // 2  # Items sell for half price
                self.coins_instance.add_coins(sell_price)
                self.item_instance.remove_item(item_name)
                print(f"Sold {item_name} for {sell_price} coins!")
                print(f"Remaining Coins: {self.coins_instance.display_coins()}")  #Display updated balance
            else:
                print("This item cannot be sold.")  #Prevents selling unrecognized items
        else:
            print("You do not have this item to sell.")  #Handles trying to sell non-owned items


# Class to manage multipliers for winnings and purchases
class Upgrades:
    def __init__(self, winning_multiplier=1.0, purchase_multiplier=1.0):
        self.winning_multiplier = winning_multiplier
        self.purchase_multiplier = purchase_multiplier

    def add_winning_multiplier(self):  # Increases winnings multiplier
        self.winning_multiplier += 0.1

    def add_purchase_multiplier(self):  # Decreases cost of purchases but caps at 0.1
        if self.purchase_multiplier > 0.1:
            self.purchase_multiplier -= 0.05
            if self.purchase_multiplier < 0.1:
                self.purchase_multiplier = 0.1  # Prevents purchase multiplier from going below 0.1
        else:
            print("Purchase Multiplier has reached the minimum limit (0.1).")

    def display_both(self):  # Displays both multipliers
        return self.winning_multiplier, self.purchase_multiplier
