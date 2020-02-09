'''
Python module for Mopidy Pummeluff tags.
'''

__all__ = (
    'Tracklist',
    'Volume',
    'PlayPause',
    'Stop',
    'Shutdown',
)

from .tracklist import Tracklist
from .volume import Volume
from .play_pause import PlayPause
from .stop import Stop
from .shutdown import Shutdown

TAGS = {}
for tag in __all__:
    TAGS[tag] = globals()[tag].__doc__.strip()
