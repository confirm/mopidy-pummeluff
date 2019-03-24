# -*- coding: utf-8 -*-
'''
Python module for the dedicated Mopidy Pummeluff threads.
'''

from __future__ import absolute_import, unicode_literals, print_function

__all__ = (
    'GPIOHandler',
)

from threading import Thread
from logging import getLogger

import RPi.GPIO as GPIO

from mopidy_pummeluff.actions import shutdown, play_pause
from mopidy_pummeluff.sound import play_sound

LOGGER = getLogger(__name__)


class GPIOHandler(Thread):
    '''
    Thread which handles the GPIO ports, which basically means activating the
    LED when it's started and then reacting to button presses.
    '''
    button_pins = {
        11: shutdown,
        12: play_pause,
    }

    led_pin = 7

    def __init__(self, core, stop_event):
        '''
        Class constructor.

        :param mopidy.core.Core core: The mopidy core instance
        :param threading.Event stop_event: The stop event
        '''
        super(GPIOHandler, self).__init__()
        self.core       = core
        self.stop_event = stop_event

    # pylint: disable=no-member
    def init_gpio(self):
        '''
        Initialize the GPIO button pins and LED pin.
        '''
        GPIO.setmode(GPIO.BOARD)

        for pin in self.button_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.HIGH)

    def run(self):
        '''
        Run the thread.
        '''
        GPIO.setmode(GPIO.BOARD)

        def callback(pin):  # pylint: disable=missing-docstring
            play_sound('success.wav')
            self.button_pins[pin](self.core)

        for pin in self.button_pins.values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=callback)

        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.HIGH)

        self.stop_event.wait()
        GPIO.cleanup()  # pylint: disable=no-member
