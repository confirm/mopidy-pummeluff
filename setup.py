#!/usr/bin/env python
'''
Setup script for Mopidy-Pummeluff module.
'''

from __future__ import absolute_import, unicode_literals

from setuptools import setup, find_packages

setup(
    name='Mopidy-Pummeluff',
    use_scm_version=True,
    url='https://git.confirm.ch/dbarton/pummeluff.git',
    license='MIT',
    author='dbarton',
    description='Mopidy Pummeluff',
    long_description=open('README.md').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=[
        'setuptools',
        'Mopidy >= 2.2.2',
    ],
    entry_points={
        b'mopidy.ext': [
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
