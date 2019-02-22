# -*- coding: utf8 -*-
'''
Python card reader module.
'''

from __future__ import absolute_import, unicode_literals, print_function

from RPi.GPIO import cleanup
from pirc522 import RFID


class ReadError(Exception):
    '''
    Exception which is thrown when the UID could not be read from the card.
    '''


class RFIDReader(RFID):
    '''
    Card reader for the RC522 RFID card reader board, based on the excellent
    :py:class:`pirc522.RFID` class.
    '''

    @staticmethod
    def cleanup():
        '''
        Cleanup GPIO ports.
        '''
        cleanup()

    @property
    def uid(self):
        '''
        Return the UID from the card.

        :return: The hex UID
        :rtype: string
        '''
        error, data = self.request()  # pylint: disable=unused-variable
        if error:
            raise ReadError('Could not read tag')

        error, uid_chunks = self.anticoll()
        if error:
            raise ReadError('Could not read UID')

        uid = '{0[0]:02X}{0[1]:02X}{0[2]:02X}{0[3]:02X}'.format(uid_chunks)
        return uid
