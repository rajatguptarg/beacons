#!/usr/bin/env python
import os
import sys
import time
import unittest
from setuptools import Command
from distutils.core import setup


def get_files(root):
    for dirname, dirnames, filenames in os.walk(root):
        for filename in filenames:
            yield os.path.join(dirname, filename)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class SQLiteTest(Command):
    """
    Run the tests on SQLite
    """
    description = "Run tests on SQLite"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(self.distribution.tests_require)

        os.environ['DATABASE_URI'] = 'sqlite://'
        os.environ['DB_NAME'] = ':memory:'

        from tests import suite
        test_result = unittest.TextTestRunner(verbosity=2).run(suite())

        if test_result.wasSuccessful():
            sys.exit(0)
        sys.exit(-1)


class PostgresTest(Command):
    """
    Run the tests on Postgres.
    """
    description = "Run tests on Postgresql"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(self.distribution.tests_require)

        os.environ['DATABASE_URI'] = 'postgresql://'
        os.environ['DB_NAME'] = 'test_' + str(int(time.time()))

        from tests import suite
        test_result = unittest.TextTestRunner(verbosity=2).run(suite())

        if test_result.wasSuccessful():
            sys.exit(0)
        sys.exit(-10)


MODULE2PREFIX = {
    'beacon_manager': 'me',
}

MODULE = "beacon_manager"
PREFIX = "my"


setup(
    name='%s_%s' % (PREFIX, MODULE),
    version='1.0',
    packages=['tests', 'beacons', 'beacons.portal'],
    url='https://www.github.com/rajatguptarg/beacons',
    license='MIT',
    author='Rajat Gupta',
    author_email='rajat.gupta712@gmail.com',
    description='Beacon Manager',
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Flask',
        'Topic :: Office/Business',
    ],
    test_suite='tests.suite',
    tests_require=[],
    cmdclass={
        'test': SQLiteTest,
        'test_postgres': PostgresTest,
    },
)
