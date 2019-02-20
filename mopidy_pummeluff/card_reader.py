#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Python card reader module.
'''

from __future__ import absolute_import, unicode_literals, print_function

from sys import exit
from signal import signal, SIGINT, SIGTERM
from time import time
from logging import getLogger
from urllib import urlopen

from RPi.GPIO import cleanup

from .MFRC522 import MFRC522

LOGGER = getLogger(__name__)


def cleanup_handler(signal, frame):
    '''
    Cleanup handler which is run when a SIGTERM or SIGINT is received.
    '''
    cleanup()
    exit()


signal(SIGINT, cleanup_handler)
signal(SIGTERM, cleanup_handler)


class UIDReadError(Exception):
    '''
    Exception which is thrown when the UID could not be read from the card.
    '''


class CardReader(MFRC522):
    '''
    Card reader for the RC522 RFID card reader board.
    '''

    def wait_for_card(self):
        '''
        Blocking method which is waiting for the card.
        '''
        LOGGER.debug('Waiting for card')
        while True:
            status, tag_type = self.MFRC522_Request(reader.PICC_REQIDL)
            if status == self.MI_OK:
                break
        LOGGER.debug('Card detected')

    @property
    def uid(self):
        '''
        Return the UID from the card.

        :return: The hex UID
        :rtype: string
        '''
        LOGGER.debug('Reading UID')

        status, uid_chunks = self.MFRC522_Anticoll()

        if status == self.MI_OK:
            uid = '{0[0]:02X}{0[1]:02X}{0[2]:02X}{0[3]:02X}'.format(uid_chunks)
            LOGGER.info('Card UID %s read', uid)
            return uid

        else:
            error = 'Could not read UID from card'
            LOGGER.warning(error)
            raise UIDReadError(error)


if __name__ == '__main__':

    reader    = CardReader()
    prev_time = time()
    prev_uid  = ''

    while True:

        reader.wait_for_card()

        try:
            now = time()
            uid = reader.uid

            if now - prev_time > 1 or uid != prev_uid:
                LOGGER.debug('Sending UID to Pummeluff HTTP API')
                response = urlopen(url='http://localhost:6880/pummeluff/card/', data=uid).read()
                LOGGER.info('UID sent to Pummeluff HTTP API')

            prev_uid  = uid
            prev_time = now

        except UIDReadError:
            pass
