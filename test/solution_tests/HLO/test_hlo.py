import unittest

from solutions.CHK import checkout_solution


class TestCheckout(unittest.TestCase):
    def test_checkout_simple(self):
        self.assertEqual(checkout_solution("A"), 50)
        self.assertEqual(checkout_solution("B"), 30)
        self.assertEqual(checkout_solution("C"), 20)
        self.assertEqual(checkout_solution("D"), 15)


