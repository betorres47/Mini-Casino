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
        self.cheese_flakes = 0

    def add_cheese(self, amount):
        self.cheese_slices += amount

    def remove_cheese(self, amount):
        if self.cheese_slices >= amount:
            self.cheese_slices -= amount
        else:
            print("Not enough cheese slices")

    def display_cheese(self):
        return {"Cheese Slices": self.cheese_slices, "Cheese Flakes": self.cheese_flakes}


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

    def buying(self, item_name, quantity=1):
        if quantity <= 0:
            print("Invalid quantity. Please enter a positive number.")
            return

        if item_name in self.shop_inventory:
            price = self.shop_inventory[item_name] * quantity
            if self.coins_instance.coins >= price:
                self.coins_instance.remove_coins(price)
                if item_name == "Prize Multiplier Upgrade":
                    self.upgrades_instances.add_winning_multiplier()
                    self.shop_inventory[item_name] = int(self.shop_inventory[item_name] * 1.5)
                elif item_name == "Purchase Multiplier Upgrade":
                    self.upgrades_instances.add_purchase_multiplier()
                    self.shop_inventory[item_name] = int(self.shop_inventory[item_name] * 1.5)
                elif item_name in ["Free Bailout", "Prize Doubler", "Random Prize Multiplier"]:
                    self.item_instance.add_items(item_name, quantity)
                elif item_name == "Cheese Wheel":
                    self.cheese_instance.add_cheese(quantity * 1000)
                elif item_name == "Huge Cheese Wheel":
                    self.cheese_instance.add_cheese(quantity * 10000)

                print(f"Successfully purchased {quantity} {item_name}(s)!")
            else:
                print("You don't have enough coins to buy!")
        else:
            print("This item is not available in the shop!")

    def selling(self, item_name):
        if item_name in self.item_instance.items and self.item_instance.items[item_name] > 0:
            if item_name in self.shop_inventory:  # Ensure it's a valid shop item
                sell_price = self.shop_inventory[item_name] // 2  # Sell for half price
            else:
                print("You cannot sell this item.")
                return

            self.coins_instance.add_coins(sell_price)
            self.item_instance.remove_item(item_name)
            print(f"Successfully sold {item_name} for {sell_price} coins!")
        else:
            print(f"You don't have any {item_name} to sell.")

    def display_shop(self):
        print("\n===== Shop Inventory =====")
        for index, (item, price) in enumerate(self.shop_inventory.items(), start=1):
            print(f"{index}. {item} - {price} coins")
