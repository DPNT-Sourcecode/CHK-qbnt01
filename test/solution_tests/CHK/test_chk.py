import unittest

from solutions.CHK import checkout_solution


class TestLoadPrices(unittest.TestCase):
    def test_load_prices(self):
        prices, deals = checkout_solution.load_prices()
        self.assertEqual(len(prices), 5)
        self.assertEqual(len(deals), 4)


class TestParseDealCode(unittest.TestCase):
    def test_parse_deal_code(self):
        self.assertEqual(checkout_solution.parse_deal_code("A"), (1, "A"))
        self.assertEqual(checkout_solution.parse_deal_code("3A"), (3, "A"))

    def test_parse_deal_code_invalid_fmt(self):
        self.assertEqual(checkout_solution.parse_deal_code(
            "3A3"), (None, None)
        )


class TestCalculateSaving(unittest.TestCase):
    def test_calc_saving_get_one_free(self):
        item_prices = {'A': 50, 'C': 20, 'B': 30, 'E': 40, 'D': 15}
        deal = '2E get one B free'
            
        saving = checkout_solution.calculate_saving(deal, item_prices)
        self.assertEqual(saving, (['2E', 'B'], 30, 80))

    def test_calc_saving_x_for(self):
        item_prices = {'A': 50, 'C': 20, 'B': 30, 'E': 40, 'D': 15}
        deal = '5A for 200'
            
        saving = checkout_solution.calculate_saving(deal, item_prices)
        self.assertEqual(saving, (['5A'], 50, 200))


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
        deal_quantity, deal_price = checkout_solution.get_deal_info(
            "A for 25", "B"
        )
        self.assertEqual(deal_quantity, None)
        self.assertEqual(deal_price, None)

    def test_get_deal_info_invalid(self):
        deal_quantity, deal_price = checkout_solution.get_deal_info(
            "2A for price of 80", "A"
        )
        self.assertEqual(deal_quantity, None)
        self.assertEqual(deal_price, None)


class TestCheckout(unittest.TestCase):
    def test_checkout_empty(self):
        self.assertEqual(checkout_solution.checkout(""), 0)

    def test_checkout_simple(self):
        self.assertEqual(checkout_solution.checkout("A"), 50)
        self.assertEqual(checkout_solution.checkout("B"), 30)
        self.assertEqual(checkout_solution.checkout("C"), 20)
        self.assertEqual(checkout_solution.checkout("D"), 15)

    def test_checkout_deal(self):
        self.assertEqual(checkout_solution.checkout("AA"), 100) # 2
        self.assertEqual(checkout_solution.checkout("AAA"), 130) # 3
        self.assertEqual(checkout_solution.checkout("AAAA"), 180) # 4
        self.assertEqual(checkout_solution.checkout("AAAAA"), 200) # 5
        self.assertEqual(checkout_solution.checkout("AAAAAA"), 250) # 6
        self.assertEqual(checkout_solution.checkout("AAAAAAAA"), 330) # 8

    def test_checkout_multiple_items(self):
        self.assertEqual(checkout_solution.checkout("AB"), 80)
        self.assertEqual(checkout_solution.checkout("ABCD"), 115)

    def test_checkout_multiple_deals(self):
        self.assertEqual(checkout_solution.checkout("AAAABBBC"), 180 + 75 + 20)
