'''
Python module for Mopidy Pummeluff tracklist tag.
'''

__all__ = (
    'Tracklist',
)

from mopidy_pummeluff.actions import replace_tracklist
from .base import Tag


class Tracklist(Tag):
    '''
    Replaces the current tracklist with the URI retreived from the tag's
    parameter.
    '''

    action = replace_tracklist
