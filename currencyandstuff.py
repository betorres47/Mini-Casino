import math

class Item:
    def __init__(self):
        self.items = {}

    def add_items(self, item_name, quantity):
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity

    def remove_item(self, item_name):
        if item_name in self.items and self.items[item_name] > 0:
            self.items[item_name] -= 1
            if self.items[item_name] == 0:
                del self.items[item_name]
        else:
            print(f"Item {item_name} was not found")

    def display_items(self):
        return self.items


class Cheese:
    def __init__(self):
        self.cheese_slices = 0

    def add_cheese(self, amount):
        self.cheese_slices += amount

    def remove_cheese(self, amount):
        if self.cheese_slices >= amount:
            self.cheese_slices -= amount
        else:
            print("Not enough cheese slices")

    def display_cheese(self):
        return {"Cheese Slices": self.cheese_slices}


class Coins:
    def __init__(self, total_coins=200):
        self.coins = total_coins

    def add_coins(self, amount):
        self.coins += amount
        self.coins = math.floor(self.coins * 100) / 100

    def remove_coins(self, amount):
        if self.coins >= amount:
            self.coins -= amount
            self.coins = math.floor(self.coins * 100) / 100
        else:
            print("You don't have enough coins to buy!")

    def display_coins(self):
        return self.coins


class Shop:
    def __init__(self, coins_instance, item_instance, cheese_instance, upgrades_instances):
        self.coins_instance = coins_instance
        self.item_instance = item_instance
        self.cheese_instance = cheese_instance
        self.upgrades_instances = upgrades_instances
        self.shop_inventory = {
            "Prize Multiplier Upgrade": 10000,
            "Purchase Multiplier Upgrade": 10000,
            "Cheese Wheel": 2000,
            "Huge Cheese Wheel": 15000,
            "Free Bailout": 50000,
            "Prize Doubler": 10000,
            "Random Prize Multiplier": 1000,
        }
        self.special_items = {
            "Super Cool Trophy": 100000000
        }

    def display_shop(self):
        print("\n===== Shop Inventory =====")
        print(f"Total Coins: {self.coins_instance.display_coins()} coins")
        print(f"Total Cheese Slices: {self.cheese_instance.cheese_slices}")

        for index, (item, price) in enumerate(self.shop_inventory.items(), start=1):
            print(f"{index}. {item} - {price} coins")

        print("\n===== Special Items (Cheese Slices Only) =====")
        for index, (item, price) in enumerate(self.special_items.items(), start=len(self.shop_inventory) + 1):
            print(f"{index}. {item} - {price} cheese slices")

        while True:
            item_choice = input("Enter item number or name to buy, type 'sell' to sell, or 'exit' to leave: ").strip()

            if item_choice.lower() == "exit":
                break
            elif item_choice.lower() == "sell":
                sell_item = input("Enter the item name to sell: ").strip()
                self.selling(sell_item)
            elif item_choice.isdigit():
                item_index = int(item_choice) - 1
                if 0 <= item_index < len(self.shop_inventory):
                    item_name = list(self.shop_inventory.keys())[item_index]
                    quantity = int(input("Enter quantity: "))
                    self.buying(item_name, quantity)
                elif len(self.shop_inventory) <= item_index < len(self.shop_inventory) + len(self.special_items):
                    special_item_name = list(self.special_items.keys())[item_index - len(self.shop_inventory)]
                    self.buy_special_item(special_item_name)
                else:
                    print("Invalid item number!")
            else:
                quantity = int(input("Enter quantity: "))
                self.buying(item_choice, quantity)

    def buying(self, item_name, quantity=1):
        """Handles purchasing items while ensuring multipliers do not appear in inventory."""
        if item_name in self.special_items:
            if self.cheese_instance.cheese_slices >= self.special_items[item_name]:
                self.cheese_instance.remove_cheese(self.special_items[item_name])
                self.item_instance.add_items(item_name, 1)
                print(f"Successfully purchased {item_name}!")
            else:
                print("You don't have enough cheese slices!")
            return

        if item_name in self.shop_inventory:
            if item_name in ["Prize Multiplier Upgrade", "Purchase Multiplier Upgrade"]:
                quantity = 1  #Force quantity to 1 for multipliers

            base_price = self.shop_inventory[item_name] * quantity
            final_price = base_price * self.upgrades_instances.purchase_multiplier

            if self.coins_instance.coins >= final_price:
                self.coins_instance.remove_coins(final_price)

                # Apply effects directly for multipliers, do NOT store them in inventory
                if item_name == "Prize Multiplier Upgrade":
                    self.upgrades_instances.add_winning_multiplier()
                elif item_name == "Purchase Multiplier Upgrade":
                    self.upgrades_instances.add_purchase_multiplier()
                else:
                    self.item_instance.add_items(item_name, quantity)

                print(f"Successfully purchased {quantity} {item_name}(s) for {final_price:.2f} coins!")
            else:
                print("You don't have enough coins!")

    def buy_special_item(self, item_name):
        """Handles buying special items using cheese slices."""
        if item_name in self.special_items:
            price = self.special_items[item_name]
            if self.cheese_instance.cheese_slices >= price:
                self.cheese_instance.remove_cheese(price)
                self.item_instance.add_items(item_name, 1)
                print(f"Successfully purchased {item_name}!")
            else:
                print("You don't have enough cheese slices!")
        else:
            print("This item is not available in the shop!")

    def selling(self, item_name):
        """Handles selling items back to the shop, ensuring multipliers cannot be sold."""
        if item_name in ["Prize Multiplier Upgrade", "Purchase Multiplier Upgrade"]:
            print("You cannot sell upgrades!")
            return

        if item_name in self.item_instance.items and self.item_instance.items[item_name] > 0:
            if item_name in self.shop_inventory:
                sell_price = self.shop_inventory[item_name] // 2
                self.coins_instance.add_coins(sell_price)
                self.item_instance.remove_item(item_name)
                print(f"Sold {item_name} for {sell_price} coins!")
            else:
                print("This item cannot be sold.")



class Upgrades:
    """Handles upgrades for prize multipliers and purchase discounts."""

    def __init__(self, winning_multiplier=1.0, purchase_multiplier=1.0):
        self.winning_multiplier = winning_multiplier
        self.purchase_multiplier = purchase_multiplier

    def add_winning_multiplier(self):
        """Increases the player's winnings multiplier."""
        self.winning_multiplier += 0.1

    def add_purchase_multiplier(self):
        """Decreases the cost of purchases."""
        self.purchase_multiplier -= 0.05

    def display_both(self):
        """Returns both multipliers."""
        return self.winning_multiplier, self.purchase_multiplier
