import unittest

# Define your test classes
class TestClass1(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(2 + 2, 4)

    def test_subtraction(self):
        self.assertEqual(5 - 3, 2)

class TestClass2(unittest.TestCase):
    def test_multiplication(self):
        self.assertEqual(2 * 3, 6)

    def test_division(self):
        self.assertEqual(10 / 2, 5)

# Test runner class
class MultiTestClassRunner:
    def __init__(self):
        self.loader = unittest.TestLoader()
        self.runner = unittest.TextTestRunner(verbosity=2)

    def run_tests(self):
        test_classes = [TestClass1, TestClass2]

        # Create test suites for each test class
        test_suites = [self.loader.loadTestsFromTestCase(test_class) for test_class in test_classes]

        # Combine all test suites into a single test suite
        all_tests_suite = unittest.TestSuite(test_suites)

        # Run all tests
        self.runner.run(all_tests_suite)

if __name__ == "__main__":
    test_runner = MultiTestClassRunner()
    test_runner.run_tests()
