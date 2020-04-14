'''
Python module for Mopidy Pummeluff shutdown tag.
'''

__all__ = (
    'Shutdown',
)

from logging import getLogger
from os import system

from .base import Action

LOGGER = getLogger(__name__)


class Shutdown(Action):
    '''
    Shutting down the system.
    '''

    @classmethod
    def execute(cls, core):
        '''
        Shutdown.

        :param mopidy.core.Core core: The mopidy core instance
        '''
        LOGGER.info('Shutting down')
        system('sudo /sbin/shutdown -h now')
