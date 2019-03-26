# -*- coding: utf-8 -*-
'''
Python module for Mopidy Pummeluff registry.
'''

from __future__ import absolute_import, unicode_literals, print_function

__all__ = (
    'RegistryDict',
    'REGISTRY',
)

import os
import json
from logging import getLogger


LOGGER = getLogger(__name__)


class RegistryDict(dict):
    '''
    Simple tag registry based on Python's internal :py:class:`dict` class,
    which reads and writes the registry from/to disk.
    '''

    registry_path = '/var/lib/mopidy/pummeluff/tags.json'

    def __init__(self):
        super(RegistryDict, self).__init__(self)

        if os.path.exists(self.registry_path):
            self.read()
        else:
            LOGGER.warning('Registry not existing yet on "%s"', self.registry_path)

    def __getitem__(self, key):
        return super(RegistryDict, self).__getitem__(str(key))

    def __setitem__(self, key, item):
        super(RegistryDict, self).__setitem__(str(key), item)
        self.write()

    def get(self, key, default=None):
        '''
        Return the value for ``key`` if ``key`` is in the dictionary, else
        ``default``.

        :param str key: The key
        :param default: The default value
        :type default: mixed

        :return: The value
        :rtype: mixed
        '''
        return super(RegistryDict, self).get(str(key), default)

    def read(self):
        '''
        Read registry from disk.

        :raises IOError: When registry file on disk is missing
        '''
        LOGGER.debug('Reading registry from %s', self.registry_path)

        with open(self.registry_path) as f:
            data = json.load(f)
            self.clear()
            self.update(data)

    def write(self):
        '''
        Write registry to disk.
        '''
        LOGGER.debug('Writing registry to %s', self.registry_path)

        config    = self.registry_path
        directory = os.path.dirname(config)

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(config, 'w') as f:
            json.dump(self, f, indent=4)


REGISTRY = RegistryDict()
