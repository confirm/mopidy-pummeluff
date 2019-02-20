# -*- coding: utf-8 -*-
'''
Python module for Mopidy Pummeluff web classes.
'''

from __future__ import absolute_import, unicode_literals

__all__ = (
    'Card',
)

from time import time
from json import dumps
from logging import getLogger

from tornado.web import RequestHandler

from .cards import Card


LOGGER = getLogger(__name__)


class CardRequestHandler(RequestHandler):
    '''
    Request handler for the card API endpoint.
    '''
    last_scan = {}

    def initialize(self, core):
        '''
        Initialize request handler with Mopidy core.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        self.core = core

    def write_response(self, data={}, error=None):
        self.set_header('Content-type', 'application/json')

        if error:
            self.set_status(400)

        data.update({
            'success': not error,
            'message': error or 'Request successful'
        })

        self.write(dumps(data))

    def get(self):
        '''
        Handle GET request, which will simply respond with the last scanned
        card.
        '''
        last_scan = CardRequestHandler.last_scan
        LOGGER.debug('Returning last scanned card with UID %s', last_scan.get('uid'))
        self.write_response(data=last_scan)

    def post(self):
        '''
        Handle POST request, which will do two things:

            - Store the card for later use (e.g. a GET method)
            - Run the action linked to the card in case it's registered
        '''
        uid = self.request.body.strip()
        LOGGER.info('Scanned card with UID "%s"', uid)

        if uid:
            card = Card(uid)

            if card.registered:
                LOGGER.info('Card is registered, triggering action')
                card.action(mopidy_core=self.core)
            else:
                LOGGER.info('Card is not registered, doing nothing')

            CardRequestHandler.last_scan = {
                'time': time(),
                'uid': card.uid,
                'instance': card
            }

            self.write_response(data=CardRequestHandler.last_scan)

        else:
            self.write_response(error='No UID in body found')
