'''
Python module for the dedicated Mopidy Pummeluff threads.
'''

__all__ = (
    'TagReader',
)

from threading import Thread
from time import time
from logging import getLogger

import RPi.GPIO as GPIO
from pirc522 import RFID

from mopidy_pummeluff.registry import REGISTRY
from mopidy_pummeluff.actions.base import Action
from mopidy_pummeluff.sound import play_sound

LOGGER = getLogger(__name__)


class ReadError(Exception):
    '''
    Exception which is thrown when an RFID read error occurs.
    '''


class TagReader(Thread):
    '''
    Thread which reads RFID tags from the RFID reader.

    Because the RFID reader algorithm is reacting to an IRQ (interrupt), it is
    blocking as long as no tag is touched, even when Mopidy is exiting. Thus,
    we're running the thread as daemon thread, which means it's exiting at the
    same moment as the main thread (aka Mopidy core) is exiting.
    '''
    daemon = True
    latest = None

    def __init__(self, core, stop_event):
        '''
        Class constructor.

        :param mopidy.core.Core core: The mopidy core instance
        :param threading.Event stop_event: The stop event
        '''
        super().__init__()
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
                    LOGGER.info('Tag %s read', uid)
                    self.handle_uid(uid)

                prev_time = now
                prev_uid  = uid

            except ReadError:
                pass

        GPIO.cleanup()  # pylint: disable=no-member

    def read_uid(self):
        '''
        Return the UID from the tag.

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
        Handle the scanned tag / retreived UID.

        :param str uid: The UID
        '''
        try:
            action = REGISTRY[str(uid)]
            LOGGER.info('Triggering action of registered tag')
            play_sound('success.wav')
            action(self.core)

        except KeyError:
            LOGGER.info('Tag is not registered, thus doing nothing')
            play_sound('fail.wav')
            action = Action(uid=uid)

        action.scanned   = time()
        TagReader.latest = action
