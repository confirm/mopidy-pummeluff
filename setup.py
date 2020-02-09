#!/usr/bin/env python
'''
Setup script for Mopidy-Pummeluff module.
'''

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().strip().split('\n')

with open('requirements_dev.txt') as f:
    requirements_dev = f.read().strip().split('\n')

setup(
    name='Mopidy-Pummeluff',
    use_scm_version=True,
    url='https://github.com/confirm/mopidy-pummeluff',
    license='MIT',
    author='confirm IT solutions',
    author_email='mopidy-pummeluff@confirm.ch',
    description='Pummeluff is a Mopidy extension which allows you to control Mopidy via RFID tags',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=[
        'tests',
        'tests.*',
    ]),
    zip_safe=False,
    include_package_data=True,
    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=['setuptools'] + requirements,
    extras_require={
        'develop': requirements_dev,
    },
    entry_points={
        'mopidy.ext': [
            'pummeluff = mopidy_pummeluff:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
