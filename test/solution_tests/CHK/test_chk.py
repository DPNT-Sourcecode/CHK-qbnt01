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
        deal_quantity, deal_price = checkout_solution.get_deal_info()


class TestCheckout(unittest.TestCase):
    def test_checkout_simple(self):
        self.assertEqual(checkout_solution.checkout("A"), 50)
        self.assertEqual(checkout_solution.checkout("B"), 30)
        self.assertEqual(checkout_solution.checkout("C"), 20)
        self.assertEqual(checkout_solution.checkout("D"), 15)

