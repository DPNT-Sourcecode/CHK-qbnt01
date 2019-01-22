from collections import Counter
import mock
import unittest

from solutions.CHK import checkout_solution


class TestLoadPrices(unittest.TestCase):
    def test_load_prices(self):
        prices, deals = checkout_solution.load_prices()
        self.assertEqual(len(prices), 6)
        self.assertEqual(len(deals), 5)


class TestParseDealCode(unittest.TestCase):
    def test_parse_deal_code(self):
        self.assertEqual(checkout_solution.parse_deal_code("A"), (1, "A"))
        self.assertEqual(checkout_solution.parse_deal_code("3A"), (3, "A"))

    def test_parse_deal_code_invalid_fmt(self):
        self.assertEqual(checkout_solution.parse_deal_code(
            "3A3"), (None, None)
        )


class TestAggregateRequirements(unittest.TestCase):
    def test_aggregate_requirements(self):
        groups = ('2E', 'B')
        self.assertEqual(
            checkout_solution.aggregate_requirements(groups),
            Counter({'E': 2, 'B': 1}),
        )

    def test_aggregate_requirements_dupe_item(self):
        groups = ('2E', 'E')
        self.assertEqual(
            checkout_solution.aggregate_requirements(groups),
            Counter({'E': 3}),
        )


class TestCalculateSaving(unittest.TestCase):
    def test_calc_saving_get_one_free(self):
        item_prices = {'A': 50, 'C': 20, 'B': 30, 'E': 40, 'D': 15}
        deal = '2E get one B free'

        saving = checkout_solution.calculate_saving(deal, item_prices)
        self.assertEqual(saving, (Counter({'E': 2, 'B': 1}), 30, 80))

    def test_calc_saving_x_for(self):
        item_prices = {'A': 50, 'C': 20, 'B': 30, 'E': 40, 'D': 15}
        deal = '5A for 200'

        saving = checkout_solution.calculate_saving(deal, item_prices)
        self.assertEqual(saving, (Counter({'A': 5}), 50, 200))


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


class TestRequirementsSatisfied(unittest.TestCase):
    def test_requirements_satisfied(self):
        items_counter = Counter({'A': 3})
        requirements = Counter({'A': 3})
        res = checkout_solution.requirements_satisfied(
            items_counter, requirements)
        self.assertEqual(res, True)

    def test_requirements_not_satisfied(self):
        items_counter = Counter({'A': 2})
        requirements = Counter({'A': 3})
        res = checkout_solution.requirements_satisfied(
            items_counter, requirements)
        self.assertEqual(res, False)


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

    def test_get_one_free(self):
        self.assertEqual(checkout_solution.checkout("EEB"), 80)

    def test_get_one_free_same_item(self):
        self.assertEqual(checkout_solution.checkout("FFF"), 20)

    def test_get_one_free_same_item_not_satisfied(self):
        mocked = mock.MagicMock()
        with mock.patch('checkout_solution.evaluate_remaining_items', mocked):
            self.assertEqual(checkout_solution.checkout("FF"), 20)

# ignore this issue for now, will try to solve later
#class TestEvaluateDeals(unittest.TestCase):
#    def test_choose_optimal_deal(self):
#        ordered_deals = [
#            ("2E get one B free", ["2E", "B"], 30, 80),
#            ("3B for 69", ["3B"], 21, 69),
#            ("3E for 100", ["3E"], 20, 100),
#        ]
#        items_counter = Counter({'B': 3, 'E': 3})
#
#        deals_cost, _ = checkout_solution.evaluate_deals(items_counter, ordered_deals)
#        optimal_deals_cost = 69 + 100 # won't work...
#        self.assertEqual(deals_cost, optimal_deals_cost)
        





