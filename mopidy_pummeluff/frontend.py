# -*- coding: utf-8 -*-
'''
Python module for Mopidy Pummeluff frontend.
'''

from __future__ import absolute_import, unicode_literals, print_function

__all__ = (
    'PummeluffFrontend',
)

from threading import Event
from logging import getLogger

import pykka
from mopidy import core as mopidy_core

from .threads import GPIOHandler, CardReader


LOGGER = getLogger(__name__)


class PummeluffFrontend(pykka.ThreadingActor, mopidy_core.CoreListener):
    '''
    Pummeluff frontend which basically reacts to GPIO button pushes and touches
    of RFID cards.
    '''

    def __init__(self, config, core):  # pylint: disable=unused-argument
        super(PummeluffFrontend, self).__init__()
        self.core         = core
        self.stop_event   = Event()
        self.gpio_handler = GPIOHandler(core=core, stop_event=self.stop_event)
        self.card_reader  = CardReader(core=core, stop_event=self.stop_event)

    def on_start(self):
        '''
        Start GPIO handler & card reader threads.
        '''
        self.gpio_handler.start()
        self.card_reader.start()

    def on_stop(self):
        '''
        Set threading stop event to tell GPIO handler & card reader threads to
        stop their operations.
        '''
        self.stop_event.set()
