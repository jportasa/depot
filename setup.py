#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name = 'depot',
    version = '0.0.13-dev',
    packages = find_packages(),
    author = 'Noah Kantrowitz',
    author_email = 'noah@coderanger.net',
    description = 'Manage package repositories in the cloud.',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    license = 'Apache 2.0',
    keywords = '',
    url = 'http://github.com/coderanger/depot',
    classifiers = [
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe = False,
    install_requires = ['apache-libcloud <=0.14.1', 'docopt==0.6.1', 'six<=1.5.2', 'lockfile<=0.10.2', 'arpy<=1.1.1', 'python-gnupg<=0.3.6', 'defusedxml<=0.4.1', 'lxml<=3.3.4'],
    tests_require = ['pytest', 'pretend', 'flake8'],
    cmdclass = {'test': PyTest},
    entry_points = {
        'console_scripts': [
            'depot = depot:main',
        ],
    }
)
