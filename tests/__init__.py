import unittest
from .test_nothing import TestNothing
from .test_views import TestViews


def suite():
    """
    Define suite
    """
    test_suite = unittest.TestSuite()
    test_suite.addTests([
        unittest.TestLoader().loadTestsFromTestCase(TestNothing),
        unittest.TestLoader().loadTestsFromTestCase(TestViews),
    ])
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
