import unittest
import coverage

class CustomTextTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"[PASSED] {test.id()}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"[FAILED] {test.id()} -> {err}")

    def addError(self, test, err):
        super().addError(test, err)
        print(f"[ERROR] {test.id()} -> {err}")


class ModuleManager(unittest.TestCase):
    def __init__(self, modules):
        """
        Initializes the ModuleManager with the given list of modules to be tested.
        :param modules: List of modules to be tested.
        """
        super().__init__()
        self.modules = modules

    def run_tests(self):
        """Runs all the test methods for each module."""
        test_suite = unittest.TestSuite()

        for module in self.modules:
            test_loader = unittest.TestLoader()
            test_suite.addTests(test_loader.loadTestsFromModule(module))

        test_runner = unittest.TextTestRunner(resultclass=CustomTextTestResult)
        test_result = test_runner.run(test_suite)

        if test_result.wasSuccessful():
            print("All tests passed.")
        else:
            print(f"{test_result.errors} errors and {test_result.failures} failures occurred.")

if __name__ == "__main__":
    # Replace 'your_module1' and 'your_module2' with the names of the modules you want to test
    import tests.testbrain
    import tests.chatterbot_preprocessors
    import tests.test_dropdown
    import tests.test_comparisons
    import tests.test_loadingscreen

    modules_to_test = [
        tests.test_loadingscreen,
        tests.test_comparisons,
        tests.test_dropdown,
        tests.testbrain,
        tests.chatterbot_preprocessors
    ]
    # Create a coverage object and start measuring coverage
    cov = coverage.Coverage()
    cov.start()
    manager = ModuleManager(modules_to_test)
    manager.run_tests()

    # Stop coverage measurement
    cov.stop()

    # Generate a coverage report
    cov.report()
