# -*- coding: utf-8 -*-
'''
Python module for Mopidy Pummeluff web classes.
'''

from __future__ import absolute_import, unicode_literals

__all__ = (
    'LatestHandler',
    'RegistryHandler',
    'RegisterHandler',
)

from json import dumps
from logging import getLogger

from tornado.web import RequestHandler

from .frontend import CardReader
from .cards import Card

LOGGER = getLogger(__name__)


class LatestHandler(RequestHandler):
    '''
    Request handler which returns the latest scanned card.
    '''
    last_scan = {}

    def initialize(self, core):
        '''
        Initialize request handler with Mopidy core.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        self.core = core

    def get(self):
        '''
        Handle GET request.
        '''
        card = CardReader.latest

        LOGGER.debug('Returning latest card %s', card)

        if card is None:
            data = {
                'success': False,
                'message': 'No card scanned yet'
            }
        else:
            data = {
                'success': True,
                'message': 'Scanned card found',
            }

            data.update(card.dict)

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))


class RegistryHandler(RequestHandler):
    '''
    Request handler which returns all registered cards.
    '''
    last_scan = {}

    def initialize(self, core):
        '''
        Initialize request handler with Mopidy core.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        self.core = core

    def get(self):
        '''
        Handle GET request.
        '''
        cards = []

        for uid, card in Card.all().items():
            cards.append(card.dict)

        data = {
            'success': True,
            'message': 'Registry successfully read',
            'cards': cards
        }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))


class RegisterHandler(RequestHandler):
    '''
    Request handler which registers an RFID card in the registry.
    '''
    last_scan = {}

    def initialize(self, core):
        '''
        Initialize request handler with Mopidy core.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        self.core = core

    def post(self):
        '''
        Handle POST request.
        '''
        card = Card.register(
            uid=self.get_argument('uid'),
            alias=self.get_argument('alias', None),
            parameter=self.get_argument('parameter'),
            card_type=self.get_argument('type')
        )

        data = {
            'success': True,
            'message': 'Card successfully registered',
        }

        data.update(card.dict)

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))

    def put(self):
        '''
        Handle PUT request.
        '''
        self.post()
