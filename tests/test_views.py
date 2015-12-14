import os
import unittest
from flask import request
from beacons import app


if 'DB_NAME' not in os.environ:
    os.environ['DATABASE_URI'] = 'sqlite://'
    os.environ['DB_NAME'] = ':memory:'


class TestViews(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DATABASE_URI'] = \
            os.environ.get('DATABASE_URI') + os.environ.get('DB_NAME')
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_0000_test_list_beacons(self):
        self.assertEqual(200, 200)

    def test_0010_test_list_beacons(self):
        with app.test_request_context('/', method='GET'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            assert request.path == '/'
            assert request.method == 'GET'

    def test_0020_test_oauth(self):
        with app.test_request_context('/oauth2callback', method='GET'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            assert request.path == '/oauth2callback'
            assert request.method == 'GET'

    def test_0030_test_register_beacon(self):
        with app.test_request_context('/register', method='GET'):
            # now you can do something with the request until the
            # end of the with block, such as basic assertions:
            assert request.path == '/register'
            assert request.method == 'GET'


def suite():
    "Test suite"
    test_suite = unittest.TestSuite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestViews)
    )
    return test_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
