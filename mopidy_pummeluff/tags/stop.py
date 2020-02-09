'''
Python module for Mopidy Pummeluff stop tag.
'''

__all__ = (
    'Stop',
)

from mopidy_pummeluff.actions import stop
from .base import Tag


class Stop(Tag):
    '''
    Stops the playback.
    '''
    action        = stop
    parameterised = False
