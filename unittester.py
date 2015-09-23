import os
import unittest
import pkgutil

def discover_and_run_tests():
    # Separate output from the invoking command
    print("=" * 70)

    # use the default shared TestLoader instance
    test_loader = unittest.defaultTestLoader
    # create a TestSuite
    test_suite = unittest.TestSuite()

    #  discover all tests in .\tests directory
    ut_package_dir = os.path.abspath(os.path.join(os.path.split(__file__)[0], 'unittests'))
    for imp, modname, _ in pkgutil.walk_packages([ut_package_dir]):
        mod = imp.find_module(modname).load_module(modname)
        for test in test_loader.loadTestsFromModule(mod):
            test_suite.addTests(test)

    # use the basic test runner that outputs to sys.stderr
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)

if __name__ == "__main__":
    discover_and_run_tests()