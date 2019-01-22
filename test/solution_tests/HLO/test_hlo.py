from solutions.CHK import checkout_solution


class TestCheckout():
    def test_checkout(self):
        assert checkout_solution.checkout("Bob") == "Hello, Bob!"

    def test_hello_null(self):
        assert hello_solution.hello("") == "Hello, World!"
