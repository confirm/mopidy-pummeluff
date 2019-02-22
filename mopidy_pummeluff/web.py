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

from . import cards
from .frontend import CardReader

LOGGER = getLogger(__name__)


class LatestHandler(RequestHandler):
    '''
    Request handler which returns the latest scanned card.
    '''

    def initialize(self, core):  # pylint: disable=arguments-differ
        '''
        Initialize request handler with Mopidy core.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        self.core = core

    def get(self, *args, **kwargs):
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

    def initialize(self, core):  # pylint: disable=arguments-differ
        '''
        Initialize request handler with Mopidy core.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        self.core = core

    def get(self, *args, **kwargs):
        '''
        Handle GET request.
        '''
        cards_list = []

        for card in cards.Card.all().values():
            cards_list.append(card.dict)

        data = {
            'success': True,
            'message': 'Registry successfully read',
            'cards': cards_list
        }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))


class RegisterHandler(RequestHandler):
    '''
    Request handler which registers an RFID card in the registry.
    '''

    def initialize(self, core):  # pylint: disable=arguments-differ
        '''
        Initialize request handler with Mopidy core.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        self.core = core

    def post(self, *args, **kwargs):
        '''
        Handle POST request.
        '''
        try:
            card = cards.Card.register(
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

        except ValueError as ex:
            self.set_status(400)
            data = {
                'success': False,
                'message': str(ex)
            }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))

    def put(self, *args, **kwargs):
        '''
        Handle PUT request.
        '''
        self.post()


class TypesHandler(RequestHandler):
    '''
    Request handler which returns all card types.
    '''

    def initialize(self, core):  # pylint: disable=arguments-differ
        '''
        Initialize request handler with Mopidy core.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        self.core = core

    def get(self, *args, **kwargs):
        '''
        Handle GET request.
        '''
        types = {}

        for cls_name in cards.__all__:
            card_cls = getattr(cards, cls_name)
            if card_cls is not cards.Card:
                card_type        = cards.Card.get_type(card_cls)
                card_doc         = card_cls.__doc__.strip().split('.')[0]
                types[card_type] = card_doc

        data = {
            'success': True,
            'message': 'Types successfully retreived',
            'types': types
        }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))
