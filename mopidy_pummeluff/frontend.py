'''
Python module for Mopidy Pummeluff frontend.
'''

__all__ = (
    'PummeluffFrontend',
)

from threading import Event
from logging import getLogger

import pykka
from mopidy import core as mopidy_core

from .threads import GPIOHandler, TagReader
from .actions.base import EmptyAction


LOGGER = getLogger(__name__)


class PummeluffFrontend(pykka.ThreadingActor, mopidy_core.CoreListener):
    '''
    Pummeluff frontend which basically reacts to GPIO button pushes and touches
    of RFID tags.
    '''

    def __init__(self, config, core):  # pylint: disable=unused-argument
        super().__init__()
        self.core         = core
        self.stop_event   = Event()
        self.gpio_handler = GPIOHandler(core=core, stop_event=self.stop_event)
        self.tag_reader   = TagReader(stop_event=self.stop_event,
                             success_event=self.success_event)

    def success_event(self, action):
        '''
        Invoke the action that was stored in the registry.
        '''
        if not isinstance(action, EmptyAction):
            action(self.core)

    def on_start(self):
        '''
        Start GPIO handler & tag reader threads.
        '''
        self.gpio_handler.start()
        self.tag_reader.start()

    def on_stop(self):
        '''
        Set threading stop event to tell GPIO handler & tag reader threads to
        stop their operations.
        '''
        self.stop_event.set()

