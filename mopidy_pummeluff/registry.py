'''
Python module for Mopidy Pummeluff registry.
'''

__all__ = (
    'RegistryDict',
    'REGISTRY',
)

import os
import json
from logging import getLogger

from mopidy_pummeluff import tags


LOGGER = getLogger(__name__)


class RegistryDict(dict):
    '''
    Class which can be used to retreive and write RFID tags to the registry.
    '''

    registry_path = '/var/lib/mopidy/pummeluff/tags.json'

    def __init__(self):
        '''
        Constructor.

        Automatically reads the registry if it exists.
        '''
        super().__init__()

        if os.path.exists(self.registry_path):
            self.read()
        else:
            LOGGER.warning('Registry not existing yet on "%s"', self.registry_path)

    @classmethod
    def unserialize_item(cls, item):
        '''
        Unserialize an item from the persistent storage on filesystem to a
        native tag.

        :param tuple item: The item

        :return: The tag
        :rtype: tags.tag
        '''
        return item['uid'], cls.init_tag(**item)

    @classmethod
    def init_tag(cls, tag_class, uid, alias=None, parameter=None):
        '''
        Initialise a new tag instance.

        :param str tag_class: The tag class
        :param str uid: The RFID UID
        :param str alias: The alias
        :param str parameter: The parameter

        :return: The tag instance
        :rtype: tags.Tag
        '''
        uid       = str(uid).strip()
        tag_class = getattr(tags, tag_class)

        return tag_class(uid, alias, parameter)

    def read(self):
        '''
        Read registry from disk.

        :raises IOError: When registry file on disk is missing
        '''
        LOGGER.debug('Reading registry from %s', self.registry_path)

        with open(self.registry_path) as f:
            data = json.load(f)
            self.clear()
            self.update((self.unserialize_item(item) for item in data))

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
            json.dump([tag.as_dict() for tag in self.values()], f, indent=4)

    def register(self, tag_class, uid, alias=None, parameter=None):
        '''
        Register a new tag in the registry.

        :param str tag_class: The tag class
        :param str uid: The UID
        :param str alias: The alias
        :param str parameter: The parameter (optional)

        :return: The tag
        :rtype: tags.Tag
        '''
        LOGGER.info('Registering %s tag %s with parameter "%s"', tag_class, uid, parameter)

        tag = self.init_tag(
            tag_class=tag_class,
            uid=uid,
            alias=alias,
            parameter=parameter
        )

        tag.validate()

        self[uid] = tag
        self.write()

        return tag


REGISTRY = RegistryDict()
