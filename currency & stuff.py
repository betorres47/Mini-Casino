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
            print("Item {} was not found".format(item_name)) #FIX SOON


    def display_items(self):
        return self.items


class Cheese:
    def __init__(self): #this function just initializes the
        self.cheese_slices = 0
        self.cheese_flakes = 0


    def add_cheese(self, amount):
        total_slices = self.cheese_slices + amount
        self.cheese_slices = total_slices

    def remove_cheese(self, amount):
        if self.cheese_slices >= amount:
            self.cheese_slices -= amount
        else:
            print("Not enough cheese slices")

    def display_cheese(self):
        return{"Cheese Slices": self.cheese_slices, "Cheese Flakes": self.cheese_flakes}


class Coins:
    def __init__(self, total_coins=0):
        self.coins = total_coins

    def add_coins(self, amount):
        self.coins += amount
        self.coins = math.floor(self.coins*100)/100

    def remove_coins(self, amount):
        if self.coins >= amount:
            self.coins -= amount
            self.coins = math.floor(self.coins*100)/100
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
            "Cheese Wheel": 2000,
            "Huge Cheese Wheel": 15000

        }

    def buying(self, item_name):
        if item_name in self.shop_inventory:
            price = self.shop_inventory[item_name]
            if self.coins_instance.coins >= price:
                self.coins_instance.remove_coins(price)
                if item_name == "Prize Multiplier Upgrade":
                    self.upgrades_instances.add_winning_multiplier()
                    self.shop_inventory[item_name] = int(price*1.5)
                elif item_name == "Cheese Wheel":
                    self.cheese_instance.add_cheese("Cheese Slice",1000)
                elif item_name == "Huge Cheese Wheel":
                    self.cheese_instance.add_cheese("Cheese Slice",10000)
    def selling(self, item_name):
        if item_name in self.item_instance.items and self.item_instance.items[item_name] > 0:
            if item_name in self.shop_inventory:
                sell_price = self.shop_inventory[item_name]//2
            else:
                sell_price = 100



    def display_shop(self):
        for item, price in self.shop_inventory.items():
            print(f"{item}: {price}coins")

class Upgrades:
    def __init__(self, winning_multiplier=1, purchase_multiplier=1):
        self.winning_multiplier = winning_multiplier
        self.purchase_multiplier = purchase_multiplier
    def add_winning_multiplier(self):
        self.winning_multiplier += .1

    def add_purchase_multiplier(self):
        self.purchase_multiplier -= .05

    def display_both(self):
        return self.winning_multiplier, self.purchase_multiplier
