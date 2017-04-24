#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='NetCatKS',
    version='0.1.1b',
    description='Networking with Crossbar, Autobahn and Twisted - Kick Starter',
    author='Dimitar Dimitrov',
    author_email='targolini@gmail.com',
    url='https://github.com/dimddev/NetCatKS',
    packages=find_packages(),
    test_suite='NetCatKS',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Server Tools',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    install_requires=[
        'pyasn1',
        'Twisted==16.4',
        'autobahn==0.10.5',
        'crossbar==0.10.4',
        'lxml==3.4.4',
        'zope.component==4.2.2',
        'zope.event==4.0.3',
        'zope.interface==4.1.2',
        'xmltodict',
        'colorama'

    ],
    scripts=['bin/netcatks']
)
