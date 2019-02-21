# -*- coding: utf-8 -*-
'''
Python module for Mopidy Pummeluff web classes.
'''

from __future__ import absolute_import, unicode_literals

__all__ = (
    'LatestHandler',
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
                'scanned': card.scanned,
                'uid': card.uid,
                'alias': card.alias,
                'type': card.get_type(),
                'parameter': card.parameter,
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

        self.set_header('Content-type', 'application/json')
        self.write({
            'success': True,
            'message': 'Card successfully registered',
            'card': str(card)
        })

    def put(self):
        '''
        Handle PUT request.
        '''
        self.post()
