# -*- coding: utf-8 -*-
'''
Python module for Mopidy Pummeluff cards.
'''

from __future__ import absolute_import, unicode_literals, print_function

__all__ = (
    'Card',
    'VolumeCard',
    'TracklistCard',
    'PauseCard',
    'StopCard',
)

from logging import getLogger

from .registry import REGISTRY


LOGGER = getLogger(__name__)


class InvalidCardType(Exception):
    '''
    Exception which is thrown when an invalid card type is defined.
    '''
    pass


class Card(object):
    '''
    Base RFID card class, which will implement the factory pattern in Python's
    own :py:meth:`__new__` method.
    '''

    def __new__(cls, uid):
        '''
        Implement factory pattern and return correct card instance.
        '''
        card         = REGISTRY.get(uid, {})
        new_cls      = cls.get_class(card.get('type', ''))

        if cls is Card and cls is not new_cls:
            instance = new_cls(uid=uid)
        else:
            instance = super(Card, cls).__new__(cls, uid=uid)

        instance.registered = bool(card)
        instance.alias      = card.get('alias')
        instance.parameter  = card.get('parameter')

        return instance

    def __init__(self, uid):
        self.uid = uid

    def __str__(self):
        cls_name   = self.__class__.__name__
        identifier = self.alias or self.uid
        return '<{}: {}>'.format(cls_name, identifier)

    @staticmethod
    def get_class(card_type):
        '''
        Return class for specific card type.

        :param str card_type: The card type

        :return: The card class
        :rtype: type
        '''
        try:
            name = card_type.title() + 'Card'
            cls  = globals()[name]
            assert issubclass(cls, Card)
        except (KeyError, AssertionError):
            raise InvalidCardType('Card class for type "{}" does\'t exist.'.format(card_type))

        return cls

    @classmethod
    def get_type(cls, card_class=None):
        '''
        Return the type for a specific card class.

        :param type card_class: The card class

        :return: The card type
        :rtype: str
        '''
        return (card_class or cls).__name__[0:-4].lower()

    @classmethod
    def all(cls):
        '''
        Return all registered cards in a list.

        :return: Registered cards
        :rtype: list[Card]
        '''
        return {uid: Card(uid=uid) for uid in REGISTRY}

    @classmethod
    def register(cls, uid, alias=None, parameter=None, card_type=None):
        '''
        Register card in the registry.

        :param str uid: The card's UID
        :param str alias: The card's alias
        :param str parameter: The optional parameter
        :param str card_type: The card type
        '''

        if card_type is None:
            card_type = cls.get_type(cls)

        uid = uid.strip()
        if not uid:
            error = 'Invalid UID defined'
            LOGGER.error(error)
            raise ValueError(error)

        LOGGER.info('Registering %s card %s with parameter "%s"', card_type, uid, parameter)

        real_cls = cls.get_class(card_type)

        if real_cls == Card:
            error = 'Registering cards without explicit types are not allowed. ' \
                'Set card_type argument on Card.register() or use register() method of explicit card classes.'
            raise InvalidCardType(error)

        if hasattr(real_cls, 'validate_parameter'):
            real_cls.validate_parameter(parameter)

        REGISTRY[uid] = {
            'type': card_type,
            'alias': alias.strip(),
            'parameter': parameter.strip()
        }

        return Card.all().get(uid)

    @property
    def dict(self):
        '''
        Return the dict version of this card.

        :return: The dict version of this card
        :rtype: dict
        '''
        d = {
            'uid': self.uid,
            'alias': self.alias,
            'type': self.get_type(),
            'parameter': self.parameter,
        }

        if hasattr(self, 'scanned'):
            d['scanned'] = self.scanned

        return d


class TracklistCard(Card):
    '''
    Replaces the current tracklist with the URI retreived from the card's
    parameter.
    '''

    def action(self, mopidy_core):
        '''
        Replace tracklist and play.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        LOGGER.info('Replacing tracklist with URI "%s"', self.parameter)
        mopidy_core.tracklist.clear()
        mopidy_core.tracklist.add(uri=self.parameter)
        mopidy_core.playback.play()


class VolumeCard(Card):
    '''
    Sets the volume to the percentage value retreived from the card's parameter.
    '''

    @staticmethod
    def validate_parameter(parameter):
        '''
        Validates if the parameter is an integer between 0 and 100.

        :param mixed parameter: The parameter

        :raises: ValueError in case the parameter is invalid
        '''
        try:
            number = int(parameter)
            assert number >= 0 and number <= 100
        except (ValueError, AssertionError):
            raise ValueError('Volume parameter has to be a number between 0 and 100')

    def action(self, mopidy_core):
        '''
        Set volume.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        LOGGER.info('Setting volume to %s', self.parameter)
        try:
            mopidy_core.mixer.set_volume(int(self.parameter))
        except ValueError as ex:
            LOGGER.error(str(ex))


class StopCard(Card):
    '''
    Stops the playback.
    '''

    def action(self, mopidy_core):
        '''
        Stop playback.
        '''
        LOGGER.info('Stopping playback')
        mopidy_core.playback.stop()


class PauseCard(Card):
    '''
    Pauses or resumes the playback, based on the current state.
    '''

    def action(self, mopidy_core):
        '''
        Pause or resume the playback.
        '''
        playback = mopidy_core.playback

        if playback.get_state().get() == 'playing':
            LOGGER.info('Pausing the playback')
            playback.pause()
        else:
            LOGGER.info('Resuming the playback')
            playback.resume()
