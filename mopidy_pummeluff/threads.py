# -*- coding: utf-8 -*-
'''
Python module for the dedicated Mopidy Pummeluff threads.
'''

__all__ = (
    'GPIOHandler',
    'CardReader',
)

from __future__ import absolute_import, unicode_literals, print_function

from os import path, system
from threading import Thread
from time import time
from logging import getLogger

import RPi.GPIO as GPIO

from .rfid_reader import RFIDReader, ReadError
from .actions import shutdown, play_pause
from .cards import Card

LOGGER = getLogger(__name__)


class GPIOHandler(Thread):
    '''
    Thread which handles the GPIO ports, which basically means activating the
    LED when it's started and then reacting to button presses.
    '''
    button_pins = {
        5: shutdown,
        7: play_pause,
    }

    led_pin = 11

    def __init__(self, core, stop_event):
        '''
        Class constructor.

        :param mopidy.core.Core core: The mopidy core instance
        :param threading.Event stop_event: The stop event
        '''
        super(CardReader, self).__init__()
        self.core       = core
        self.stop_event = stop_event

    def init_gpio(self):
        '''
        Initialize the GPIO button pins and LED pin.
        '''
        GPIO.setmode(GPIO.BOARD)

        for pin in self.button_pins.keys():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.HIGH)

    def run(self):
        '''
        Run the thread.
        '''
        GPIO.setmode(GPIO.BOARD)

        def callback(pin):
            self.button_pins[pin](self.core)

        for pin in self.button_pins.values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=callback)

        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.HIGH)

        self.stop_event.wait()
        GPIO.cleanup()


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
                    LOGGER.info('Card %s read', uid)
                    self.handle_uid(uid)

                prev_time = now
                prev_uid  = uid

            except ReadError:
                pass

        reader.cleanup()

    def handle_uid(self, uid):
        '''
        Handle the scanned card / retreived UID.

        :param str uid: The UID
        '''
        card = Card(uid)

        if card.registered:
            LOGGER.info('Triggering action of registered card')
            self.play_sound('success.wav')
            card(mopidy_core=self.core)

        else:
            LOGGER.info('Card is not registered, thus doing nothing')
            self.play_sound('fail.wav')

        card.scanned      = time()
        CardReader.latest = card
