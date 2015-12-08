import unittest


class TestNothing(unittest.TestCase):
    def test_0010_test_nothing(self):
        self.assertEqual(200, 200)


def suite():
    "Test suite"
    test_suite = unittest.TestSuite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestNothing)
    )
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
