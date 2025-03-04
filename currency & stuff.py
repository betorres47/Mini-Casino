
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


class Cheeses:
    def __init__(self): #this function just initializes the
        self.cheeses = {}

    def add_cheese(self, name, quantity):
        if name in self.cheeses:
            self.cheeses[name] += quantity
        else:
            self.cheeses[name] = quantity

    def remove_cheese(self, cheese_name):
        if cheese_name in self.cheeses and self.cheeses[cheese_name] > 0:
            self.cheeses[cheese_name] -= 1
            if self.cheeses[cheese_name] == 0:
                del self.cheeses[cheese_name]
        else:
            print("Cheese {} was not found".format(cheese_name)) #FIX SOON

    def display_cheese(self):
        return self.cheeses


class Coins:
    def __init__(self, total_coins=0):
        self.coins = total_coins

    def add_coins(self, amount):
        self.coins += amount

    def remove_coins(self, amount):
        if self.coins >= amount:
            self.coins -= amount
        else:
            print("Not enough coins")

    def display_coins(self):
        return self.coins

class Shopping:
    def __init__(self, coins_instance, item_instance):
        self.coins_instance = coins_instance
        self.item_instance = item_instance
        self.shop_inventory = {""}

    def buying(self):

    def selling(self):

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
