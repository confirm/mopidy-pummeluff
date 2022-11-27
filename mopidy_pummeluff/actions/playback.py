'''
Python module for Mopidy Pummeluff playback actions.
'''

__all__ = (
    'PlayPause',
    'Stop',
    'PreviousTrack',
    'NextTrack',
)

from logging import getLogger

from .base import Action

LOGGER = getLogger(__name__)


class PlayPause(Action):
    '''
    Pause or resume the playback.
    '''

    @classmethod
    def execute(cls, core):
        '''
        Pause or resume the playback.

        :param mopidy.core.Core core: The mopidy core instance
        '''
        playback = core.playback

        if playback.get_state().get() == 'playing':
            LOGGER.info('Pausing the playback')
            playback.pause()
        else:
            LOGGER.info('Resuming the playback')
            playback.resume()


class Stop(Action):
    '''
    Stop the playback.
    '''

    @classmethod
    def execute(cls, core):
        '''
        Stop playback.

        :param mopidy.core.Core core: The mopidy core instance
        '''
        LOGGER.info('Stopping playback')
        core.playback.stop()


class PreviousTrack(Action):
    '''
    Change to the previous track.
    '''

    @classmethod
    def execute(cls, core):
        '''
        Change to previous track.

        :param mopidy.core.Core core: The mopidy core instance
        '''
        LOGGER.info('Changing to previous track')
        core.playback.previous()


class NextTrack(Action):
    '''
    Change to the next track.
    '''

    @classmethod
    def execute(cls, core):
        '''
        Change to next track.

        :param mopidy.core.Core core: The mopidy core instance
        '''
        LOGGER.info('Changing to next track')
        core.playback.next()
