# -*- coding: utf-8 -*-
'''
Python module for Mopidy Pummeluff frontend.
'''

from __future__ import absolute_import, unicode_literals, print_function

from threading import Thread, Event
from time import time
from logging import getLogger

import pykka
from mopidy import core

from .rfid_reader import RFIDReader, ReadError

LOGGER = getLogger(__name__)


class CardReader(Thread):
    '''
    Thread class which reads RFID cards from the RFID reader.
    '''
    def __init__(self, stop_event):
        '''
        Class constructor.

        :param threading.Event stop_event: The stop event
        '''
        super(CardReader, self).__init__()
        self.stop_event = stop_event

    def run(self):
        '''
        Run RFID reading loop.
        '''
        reader    = RFIDReader()
        prev_time = time()
        prev_uid  = ''

        while not self.stop_event.is_set():
            reader.wait_for_tag()

            try:
                now = time()
                uid = reader.uid

                if now - prev_time > 1 or uid != prev_uid:
                    LOGGER.info('Card with UID %s read', uid)

                prev_uid  = uid
                prev_time = now

            except ReadError:
                pass

        reader.cleanup()


class PummeluffFrontend(pykka.ThreadingActor, core.CoreListener):
    '''
    Pummeluff frontend which basically reads cards from the RFID reader.
    '''

    def __init__(self, config, core):
        super(PummeluffFrontend, self).__init__()
        self.core        = core
        self.stop_event  = Event()
        self.card_reader = CardReader(self.stop_event)

    def on_start(self):
        '''
        Start card reader thread after the actor is started.
        '''
        self.card_reader.start()

    def on_stop(self):
        '''
        Stop card reader thread before the actor stops.
        '''
        self.stop_event.set()
