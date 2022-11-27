'''
Python module for Mopidy Pummeluff registry.
'''

__all__ = (
    'RegistryDict',
    'REGISTRY',
)

import json
import os
from logging import getLogger

from mopidy_pummeluff import actions

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
        native action.

        :param tuple item: The item

        :return: The action
        :rtype: actions.Action
        '''
        if 'action_class' in item:
            item['action'] = item.pop('action_class')

        return item['uid'], cls.init_action(**item)

    @classmethod
    def init_action(cls, action, uid, alias=None, parameter=None):
        '''
        Initialise a new action instance.

        :param str action: The action class
        :param str uid: The RFID UID
        :param str alias: The alias
        :param str parameter: The parameter

        :return: The action instance
        :rtype: actions.Action
        '''
        uid    = str(uid).strip()
        action = getattr(actions, action)

        return action(uid, alias, parameter)

    def read(self):
        '''
        Read registry from disk.

        :raises IOError: When registry file on disk is missing
        '''
        LOGGER.debug('Reading registry from %s', self.registry_path)

        with open(self.registry_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
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

        with open(config, 'w', encoding='utf-8') as file:
            json.dump([action.as_dict() for action in self.values()], file, indent=4)

    def register(self, action, uid, alias=None, parameter=None):
        '''
        Register a new tag in the registry.

        :param str action: The action class
        :param str uid: The UID
        :param str alias: The alias
        :param str parameter: The parameter (optional)

        :return: The action instance
        :rtype: actions.Action

        :raises ValueError: When UID is not defined
        '''
        LOGGER.info('Registering %s tag %s with parameter "%s"', action, uid, parameter)

        if not uid:
            raise ValueError('UID required to register a tag')

        action_instance = self.init_action(
            action=action,
            uid=uid,
            alias=alias,
            parameter=parameter
        )

        action_instance.validate()

        self[uid] = action_instance
        self.write()

        return action_instance

    def unregister(self, uid):
        '''
        Unregister a tag from the registry.

        :param str uid: The UID

        :raises ValueError: When UID is not defined
        '''
        if not uid:
            raise ValueError('UID required to unregister a tag')

        LOGGER.info('Unregistering tag %s', uid)

        if uid not in self:
            raise ValueError('UID not registered')

        del self[uid]
        self.write()


REGISTRY = RegistryDict()
