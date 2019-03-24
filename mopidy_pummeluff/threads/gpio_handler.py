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
from time import time

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
        5: shutdown,
        7: play_pause,
    }

    led_pin = 8

    def __init__(self, core, stop_event):
        '''
        Class constructor.

        :param mopidy.core.Core core: The mopidy core instance
        :param threading.Event stop_event: The stop event
        '''
        super(GPIOHandler, self).__init__()

        self.core       = core
        self.stop_event = stop_event

        now             = time()
        self.timestamps = {x: now for x in self.button_pins}

    # pylint: disable=no-member
    def run(self):
        '''
        Run the thread.
        '''
        GPIO.setmode(GPIO.BOARD)

        for pin in self.button_pins:
            LOGGER.debug('Setup pin %s as button pin', pin)
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.RISING, callback=lambda pin: self.button_push(pin))  # pylint: disable=unnecessary-lambda

        LOGGER.debug('Setup pin %s as LED pin', self.led_pin)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.HIGH)

        self.stop_event.wait()
        GPIO.cleanup()  # pylint: disable=no-member

    def button_push(self, pin):
        '''
        Callback method when a button is pushed.

        :param int pin: Pin number
        '''
        now    = time()
        before = self.timestamps[pin]

        if (GPIO.input(pin) == GPIO.LOW) and (now - before > 0.25):
            LOGGER.debug('Button at pin %s was pushed', pin)
            play_sound('success.wav')
            self.button_pins[pin](self.core)
            self.timestamps[pin] = now
