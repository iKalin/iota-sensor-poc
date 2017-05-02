# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='iota_sensor',
    version='0.1',
    description=('POC script to read sensor data from the public NetAtmo API '
                 'and attach it to the IOTA Tangle.'),
    url='https://github.com/ivoscc/iota-sensor-poc',
    install_requires=[
        'pyota',
        'requests',
        'six',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'iota-sensor=iota_sensor.poc:main',
        ],
    },
    license = 'MIT',
)
