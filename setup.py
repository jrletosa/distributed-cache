#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='distributed-cache',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'bottle',
        'waitress',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'distributed-cache = distributed_cache:main',
        ],
    },
    zip_safe=False,
)
