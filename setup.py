import os
import re

from setuptools import setup, find_packages


def get_version():
    """ Reads package version number from package's __init__.py. """
    with open(os.path.join(
        os.path.dirname(__file__), 'monitor_mysql_overflows', '__init__.py'
    )) as init:
        for line in init.readlines():
            res = re.match(r'^__version__ = [\'"](.*)[\'"]$', line)
            if res:
                return res.group(1)


def get_long_description():
    """ Read description from README and CHANGES. """
    with open(
        os.path.join(os.path.dirname(__file__), 'README.md')
    ) as readme, open(
        os.path.join(os.path.dirname(__file__), 'CHANGES.md')
    ) as changes:
        return readme.read() + '\n' + changes.read()


setup(
    name='monitor-mysql-overflows',
    version=get_version(),
    description='MySQL utilities to detect integer like columns overflows',
    long_description=get_long_description(),
    author='Jeremy Cohen Solal',
    author_email='jeremy@rentabiliweb.com',
    url='http://www.rentabiliweb-group.com',
    packages=find_packages(),
    install_requires=[
        'mysql-python',
    ],
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: System :: Monitoring',
        'Topic :: Utilities',
    ],
    license='Proprietary',
    entry_points={
        'console_scripts': [
            'monitor-mysql-overflows = monitor_mysql_overflows:monitor',
        ],
    },
)
