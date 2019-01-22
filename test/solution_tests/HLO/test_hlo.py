from solutions.HLO import hello_solution


class TestHello():
    def test_hello(self):
        assert hello_solution.hello("Bob") == "Hello, Bob!"

    def test_hello_null(self):
        assert hello_solution.hello() == "Hello, World!"

