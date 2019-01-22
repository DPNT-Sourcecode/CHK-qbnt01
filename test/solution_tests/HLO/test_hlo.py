import unittest

from solutions.CHK import checkout_solution


class TestCheckout(unittest.TestCase):
    def test_checkout(self):
        assert checkout_solution.checkout() == None

