# -*- coding: utf-8 -*-
'''
Python module for the dedicated Mopidy Pummeluff threads.
'''

from __future__ import absolute_import, unicode_literals, print_function

__all__ = (
    'CardReader',
)

from os import path, system
from threading import Thread
from time import time
from logging import getLogger

import RPi.GPIO as GPIO
from pirc522 import RFID

from mopidy_pummeluff.cards import Card

LOGGER = getLogger(__name__)


class ReadError(Exception):
    '''
    Exception which is thrown when an RFID read error occurs.
    '''


class CardReader(Thread):
    '''
    Thread which reads RFID cards from the RFID reader.

    Because the RFID reader algorithm is reacting to an IRQ (interrupt), it is
    blocking as long as no card is touched, even when Mopidy is exiting. Thus,
    we're running the thread as daemon thread, which means it's exiting at the
    same moment as the main thread (aka Mopidy core) is exiting.
    '''
    daemon = True
    latest = None

    @staticmethod
    def play_sound(sound):
        '''
        Play sound via aplay.

        :param str sound: The name of the sound file
        '''
        file_path = path.join(path.dirname(__file__), 'sounds', sound)
        system('aplay -q {}'.format(file_path))

    def __init__(self, core, stop_event):
        '''
        Class constructor.

        :param mopidy.core.Core core: The mopidy core instance
        :param threading.Event stop_event: The stop event
        '''
        super(CardReader, self).__init__()
        self.core       = core
        self.stop_event = stop_event
        self.rfid       = RFID()

    def run(self):
        '''
        Run RFID reading loop.
        '''
        rfid      = self.rfid
        prev_time = time()
        prev_uid  = ''

        while not self.stop_event.is_set():
            rfid.wait_for_tag()

            try:
                now = time()
                uid = self.read_uid()

                if now - prev_time > 1 or uid != prev_uid:
                    LOGGER.info('Card %s read', uid)
                    self.handle_uid(uid)

                prev_time = now
                prev_uid  = uid

            except ReadError:
                pass

        GPIO.cleanup()  # pylint: disable=no-member

    def read_uid(self):
        '''
        Return the UID from the card.

        :return: The hex UID
        :rtype: string
        '''
        rfid = self.rfid

        error, data = rfid.request()  # pylint: disable=unused-variable
        if error:
            raise ReadError('Could not read tag')

        error, uid_chunks = rfid.anticoll()
        if error:
            raise ReadError('Could not read UID')

        uid = '{0[0]:02X}{0[1]:02X}{0[2]:02X}{0[3]:02X}'.format(uid_chunks)  # pylint: disable=invalid-format-index
        return uid

    def handle_uid(self, uid):
        '''
        Handle the scanned card / retreived UID.

        :param str uid: The UID
        '''
        card = Card(uid)

        if card.registered:
            LOGGER.info('Triggering action of registered card')
            self.play_sound('success.wav')
            card(self.core)

        else:
            LOGGER.info('Card is not registered, thus doing nothing')
            self.play_sound('fail.wav')

        card.scanned      = time()
        CardReader.latest = card
