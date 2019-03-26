# -*- coding: utf-8 -*-
'''
Python module for Mopidy Pummeluff tags.
'''

from __future__ import absolute_import, unicode_literals, print_function

__all__ = (
    'Tag',
    'TracklistTag',
    'VolumeTag',
    'PlayPauseTag',
    'StopTag',
    'ShutdownTag',
)

from logging import getLogger

from .registry import REGISTRY
from . import actions


LOGGER = getLogger(__name__)


class InvalidTagType(Exception):
    '''
    Exception which is thrown when an invalid tag type is defined.
    '''
    pass


class Tag(object):
    '''
    Base RFID tag class, which will implement the factory pattern in Python's
    own :py:meth:`__new__` method.
    '''
    parameter_allowed = True

    def __new__(cls, uid):
        '''
        Implement factory pattern and return correct tag instance.
        '''
        tag         = REGISTRY.get(uid, {})
        new_cls      = cls.get_class(tag.get('type', ''))

        if cls is Tag and cls is not new_cls:
            instance = new_cls(uid=uid)
        else:
            instance = super(Tag, cls).__new__(cls, uid=uid)

        instance.registered = bool(tag)
        instance.alias      = tag.get('alias')
        instance.parameter  = tag.get('parameter')

        return instance

    def __init__(self, uid):
        self.uid     = uid
        self.scanned = None

    def __str__(self):
        cls_name   = self.__class__.__name__
        identifier = self.alias or self.uid
        return '<{}: {}>'.format(cls_name, identifier)

    def __call__(self, core):
        '''
        Action method which is called when the tag is detected on the RFID
        reader.

        :param mopidy.core.Core core: The mopidy core instance
        '''
        args = [core]
        if self.parameter:
            args.append(self.parameter)
        getattr(actions, self.action)(*args)

    @staticmethod
    def get_class(tag_type):
        '''
        Return class for specific tag type.

        :param str tag_type: The tag type

        :return: The tag class
        :rtype: type
        '''
        try:
            name = tag_type.title() + 'Tag'
            cls  = globals()[name]
            assert issubclass(cls, Tag)
        except (KeyError, AssertionError):
            raise InvalidTagType('Tag class for type "{}" does\'t exist.'.format(tag_type))

        return cls

    @classmethod
    def get_type(cls, tag_class=None):
        '''
        Return the type for a specific tag class.

        :param type tag_class: The tag class

        :return: The tag type
        :rtype: str
        '''
        return (tag_class or cls).__name__[0:-3].lower()

    @classmethod
    def all(cls):
        '''
        Return all registered tags in a list.

        :return: Registered tags
        :rtype: list[Tag]
        '''
        return {uid: Tag(uid=uid) for uid in REGISTRY}

    @classmethod
    def register(cls, uid, alias=None, parameter=None, tag_type=None):
        '''
        Register tag in the registry.

        :param str uid: The tag's UID
        :param str alias: The tag's alias
        :param str parameter: The optional parameter
        :param str tag_type: The tag type

        :return: The registered tag
        :rtype: Tag
        '''

        if tag_type is None:
            tag_type = cls.get_type(cls)

        uid = uid.strip()
        if not uid:
            error = 'Invalid UID defined'
            LOGGER.error(error)
            raise ValueError(error)

        LOGGER.info('Registering %s tag %s with parameter "%s"', tag_type, uid, parameter)

        real_cls = cls.get_class(tag_type)

        if real_cls == Tag:
            error = 'Registering tags without explicit types are not allowed. ' \
                'Set tag_type argument on Tag.register() ' \
                'or use register() method of explicit tag classes.'
            raise InvalidTagType(error)

        if not real_cls.parameter_allowed and parameter:
            raise ValueError('No parameter allowed for this tag')
        elif hasattr(real_cls, 'validate_parameter'):
            real_cls.validate_parameter(parameter)

        REGISTRY[uid] = {
            'type': tag_type,
            'alias': alias.strip(),
            'parameter': parameter.strip()
        }

        return Tag.all().get(uid)

    @property
    def dict(self):
        '''
        Return the dict version of this tag.

        :return: The dict version of this tag
        :rtype: dict
        '''
        tag_dict = {
            'uid': self.uid,
            'alias': self.alias,
            'type': self.get_type(),
            'parameter': self.parameter,
        }

        tag_dict['scanned'] = self.scanned

        return tag_dict

    @property
    def action(self):
        '''
        Return a name of an action (function) defined in the
        :py:mod:`mopidy_pummeluff.actions` Python module.

        :return: An action name
        :rtype: str
        :raises NotImplementedError: When action property isn't defined
        '''
        cls   = self.__class__.__name__
        error = 'Missing action property in the %s class'
        LOGGER.error(error, cls)
        raise NotImplementedError(error % cls)


class TracklistTag(Tag):
    '''
    Replaces the current tracklist with the URI retreived from the tag's
    parameter.
    '''
    action = 'replace_tracklist'


class VolumeTag(Tag):
    '''
    Sets the volume to the percentage value retreived from the tag's parameter.
    '''
    action = 'set_volume'

    @staticmethod
    def validate_parameter(parameter):
        '''
        Validates if the parameter is an integer between 0 and 100.

        :param mixed parameter: The parameter

        :raises ValueError: When parameter is invalid
        '''
        try:
            number = int(parameter)
            assert number >= 0 and number <= 100
        except (ValueError, AssertionError):
            raise ValueError('Volume parameter has to be a number between 0 and 100')


class PlayPauseTag(Tag):
    '''
    Pauses or resumes the playback, based on the current state.
    '''
    action            = 'play_pause'
    parameter_allowed = False


class StopTag(Tag):
    '''
    Stops the playback.
    '''
    action            = 'stop'
    parameter_allowed = False


class ShutdownTag(Tag):
    '''
    Shutting down the system.
    '''
    action            = 'shutdown'
    parameter_allowed = False
