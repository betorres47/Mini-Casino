# - test files for main.py and currencyandstuff.py

import unittest
from unittest.mock import patch                     # mock serves to input 'false inputs' and read 'false outputs', patch serves to create 'fake objects' (ref. README)
from currencyandstuff import Item, Cheese, Coins, Shop, Upgrades


class TestItem(unittest.TestCase):                                                                  # test for items
    def setUp(self):                                                                                # set up zero items
        self.items = Item()

    def test_add_items(self):                                                                       # add 1 item
        self.items.add_items("Prize Multiplier Upgrade", 1)
        self.assertEqual(self.items.display_items(), {"Prize Multiplier Upgrade": 1})

    def test_remove_item(self):                                                                     # remove 1 item
        self.items.add_items("Prize Multiplier Upgrade", 1)
        self.items.remove_item("Prize Multiplier Upgrade")
        self.assertEqual(self.items.display_items(), {})

    def test_display_items(self):                                                                   # display item
        self.items.add_items("Cheese Wheel", 100)
        self.assertEqual(self.items.display_items(), {"Cheese Wheel": 100})


class TestCheese(unittest.TestCase):                                                                # test for cheese
    def setUp(self):                                                                                # set up zero cheese slices
        self.cheese = Cheese()

    def test_add_cheese(self):                                                                      # add 5 cheese slices
        self.cheese.add_cheese(5)
        self.assertEqual(self.cheese.display_cheese(), {"Cheese Slices": 5})

    def test_remove_cheese(self):                                                                   # remove 4 cheese from 10
        self.cheese.add_cheese(10)
        self.cheese.remove_cheese(4)
        self.assertEqual(self.cheese.display_cheese(), {"Cheese Slices": 6})

    def test_remove_cheese_not_enough(self):                                                        # remove too many cheeses
        self.cheese.add_cheese(5)
        self.cheese.remove_cheese(6)
        self.assertEqual(self.cheese.display_cheese(), {"Cheese Slices": 5})


class TestCoins(unittest.TestCase):                                                                 # test for coins
    def setUp(self):                                                                                # set up 5000 coins
        self.coins = Coins(5000)

    def test_add_coins(self):                                                                       # add 1000 coins
        self.coins.add_coins(1000)
        self.assertEqual(self.coins.display_coins(), 6000)

    def test_remove_coins(self):                                                                    # remove 500 coins
        self.coins.remove_coins(500)
        self.assertEqual(self.coins.display_coins(), 4500)

    def test_remove_coins_not_enough(self):                                                         # remove too many coins
        self.coins.remove_coins(6000)
        self.assertEqual(self.coins.display_coins(), 5000)


class TestShop(unittest.TestCase):
    def setUp(self):
        self.coins = Coins(50000)
        self.items = Item()
        self.cheese = Cheese()
        self.upgrades = Upgrades()
        self.shop = Shop(self.coins, self.items, self.cheese, self.upgrades)

    @patch('builtins.input', side_effect=['Prize Multiplier Upgrade'])
    @patch('builtins.print')
    def test_buy_item(self, mock_print, mock_input):
        # Test buying an item (Prize Multiplier Upgrade)
        self.shop.buying("Prize Multiplier Upgrade")
        self.assertEqual(self.coins.display_coins(), 50000 - 10000 * self.upgrades.purchase_multiplier)
        mock_print.assert_called_with("Remaining Coins: 40000")

    @patch('builtins.input', side_effect=['Cheese Wheel'])
    @patch('builtins.print')
    def test_buy_cheese_item(self, mock_print, mock_input):
        self.cheese.add_cheese(5000)
        self.shop.buying("Cheese Wheel")
        self.assertEqual(self.cheese.display_cheese(), {"Cheese Slices": 3000})  # After spending 2000 cheese slices
        mock_print.assert_called_with("Successfully purchased Cheese Wheel!")


class TestUpgrades(unittest.TestCase):
    def setUp(self):
        self.upgrades = Upgrades()

    def test_add_winning_multiplier(self):
        initial_multiplier = self.upgrades.winning_multiplier
        self.upgrades.add_winning_multiplier()
        self.assertGreater(self.upgrades.winning_multiplier, initial_multiplier)

    def test_add_purchase_multiplier(self):
        initial_multiplier = self.upgrades.purchase_multiplier
        self.upgrades.add_purchase_multiplier()
        self.assertLess(self.upgrades.purchase_multiplier, initial_multiplier)
