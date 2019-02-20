# -*- coding: utf-8 -*-
'''
Python module for Mopidy Pummeluff web classes.
'''

from __future__ import absolute_import, unicode_literals

__all__ = (
    'LatestScanHandler',
)

from json import dumps
from logging import getLogger

from tornado.web import RequestHandler

from .frontend import CardReader

LOGGER = getLogger(__name__)


class LatestScanHandler(RequestHandler):
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
        Handle GET request, which will simply respond with the latest scanned
        card.
        '''
        latest = CardReader.latest

        LOGGER.debug('Returning latest card with UID %s', latest.get('uid'))

        self.set_header('Content-type', 'application/json')
        self.write(dumps(latest))
