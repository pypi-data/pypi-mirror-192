#!/usr/bin/env python

from distutils.core import setup

setup(
    name='apport',
    version='1.0',
    description='Python data-processing utilities',
    author='Mikhalev Oleg',
    author_email='mhalairt@gmail.com',
    url='https://github.com/mhalairt/apport',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Topic :: Utilities',
    ],
    packages=[
        'apport',
    ],
    package_dir={
        'apport': 'src/apport',
    },
)

