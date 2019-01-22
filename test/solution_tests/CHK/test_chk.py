import unittest

from solutions.CHK import checkout_solution


class TestLoadPrices(unittest.TestCase):
    def test_load_prices(self):
        prices = checkout_solution.load_prices()
        self.assertEqual(len(prices), 4)


class TestParseSKU(unittest.TestCase):
    def test_parse_sku(self):
        self.assertEqual(checkout_solution.parse_sku("A"), (1, "A"))
        self.assertEqual(checkout_solution.parse_sku("3A"), (3, "A"))

    def test_parse_sku_invalid_fmt(self):
        self.assertEqual(checkout_solution.parse_sku("3A3"), (None, None))


class TestDealInfo(unittest.TestCase):
    def test_get_deal_info(self):
        deal_quantity, deal_price = checkout_solution.get_deal_info("2A for 80", "A")
        self.assertEqual(deal_quantity, 2)
        self.assertEqual(deal_price, 80)

    def test_get_deal_info_no_quantity(self):
        deal_quantity, deal_price = checkout_solution.get_deal_info("A for 25", "A")
        self.assertEqual(deal_quantity, 1)
        self.assertEqual(deal_price, 25)
        
    def test_get_deal_info_wrong_item(self):
        deal_quantity, deal_price = checkout_solution.get_deal_info("A for 25", "B")
        self.assertEqual(deal_quantity, None)
        self.assertEqual(deal_price, None)

    def test_get_deal_info_invalid(self):
        deal_quantity, deal_price = checkout_solution.get_deal_info("2A for price of 80", "A")
        self.assertEqual(deal_quantity, None)
        self.assertEqual(deal_price, None)


class TestCheckout(unittest.TestCase):
    def test_checkout_simple(self):
        self.assertEqual(checkout_solution.checkout("A"), 50)
        self.assertEqual(checkout_solution.checkout("B"), 30)
        self.assertEqual(checkout_solution.checkout("C"), 20)
        self.assertEqual(checkout_solution.checkout("D"), 15)

    def test_checkout_deal(self):
        self.assertEqual(checkout_solution.checkout("2A"), 100)
        self.assertEqual(checkout_solution.checkout("3A"), 130)
        self.assertEqual(checkout_solution.checkout("4A"), 180)
        self.assertEqual(checkout_solution.checkout("5A"), 230)
        self.assertEqual(checkout_solution.checkout("6A"), 260)

    def test_checkout_multiple_items(self):
        self.assertEqual(checkout_solution.checkout("A,B"), 80)
        self.assertEqual(checkout_solution.checkout("A,B,C,D"), 115)

    def test_checkout_multiple_deals(self):
        self.assertEqual(checkout_solution.checkout("4A,3B,C"), 180 + 75 + 20)





