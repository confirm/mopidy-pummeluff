'''
Python module for Mopidy Pummeluff play pause tag.
'''

__all__ = (
    'PlayPause',
)

from mopidy_pummeluff.actions import play_pause
from .base import Tag


class PlayPause(Tag):
    '''
    Pauses or resumes the playback, based on the current state.
    '''
    action        = play_pause
    parameterised = False
