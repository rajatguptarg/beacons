import unittest
from .test_nothing import TestNothing


def suite():
    """
    Define suite
    """
    test_suite = unittest.TestSuite()
    test_suite.addTests([
        unittest.TestLoader().loadTestsFromTestCase(TestNothing),
    ])
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
