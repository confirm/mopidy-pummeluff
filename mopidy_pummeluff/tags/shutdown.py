'''
Python module for Mopidy Pummeluff shutdown tag.
'''

__all__ = (
    'Shutdown',
)

from mopidy_pummeluff.actions import shutdown
from .base import Tag


class Shutdown(Tag):
    '''
    Shutting down the system.
    '''
    action        = shutdown
    parameterised = False
