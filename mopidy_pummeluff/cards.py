# -*- coding: utf-8 -*-
'''
Python module for Mopidy Pummeluff cards.
'''

from __future__ import absolute_import, unicode_literals

__all__ = (
    'Card',
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
        instance.parameter  = card.get('parameter')

        return instance

    def __init__(self, uid):
        self.uid = uid

    def __str__(self):
        return '<{0.__class__.__name__}: {0.uid} {0.parameter}>'.format(self)

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
            return globals()[name]
        except KeyError:
            raise InvalidCardType('Card class for type "{}" does\'t exist.'.format(card_type))

    @staticmethod
    def get_type(card_class):
        '''
        Return the type for a specific card class.

        :param type card_class: The card class

        :return: The card type
        :rtype: str
        '''
        return card_class.__name__[0:-4].lower()

    @classmethod
    def all(cls):
        '''
        Return all registered cards in a list.

        :return: Registered cards
        :rtype: list[Card]
        '''
        return {uid: Card(uid=uid) for uid in REGISTRY}

    @classmethod
    def register(cls, uid, parameter=None, card_type=None):
        '''
        Register card in the registry.

        :param str uid: The card's UID
        :param str parameter: The optional parameter
        :param str card_type: The card type
        '''

        if card_type is None:
            card_type = cls.get_type(cls)

        LOGGER.info('Registering %s card with UID "%s" and parameter "%s"', card_type, uid, parameter)

        if cls.get_class(card_type) == Card:
            error = 'Registering cards without explicit types are not allowed. ' \
                'Set card_type argument on Card.register() or use register() method of explicit card classes.'
            raise InvalidCardType(error)

        REGISTRY[uid] = {
            'type': card_type,
            'parameter': parameter
        }

        return Card.all().get(uid)


class TrackCard(Card):
    '''
    Card which is replacing the tracklist with the URI defined in the card's
    argument.
    '''

    def action(self, mopidy_core):
        '''
        Replace tracklist and play.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        LOGGER.debug('Replacing tracklist with URI "%s"', self.parameter)
        mopidy_core.tracklist.clear()
        mopidy_core.tracklist.add(uri=self.parameter)
        mopidy_core.playback.play()


class VolumeCard(Card):
    '''
    Card which is setting the volume to the value of the card's argument.
    '''

    def action(self, mopidy_core):
        '''
        Set volume.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        LOGGER.debug('Setting volume to %s', self.parameter)
        mopidy_core.mixer.set_volume(int(self.parameter))
