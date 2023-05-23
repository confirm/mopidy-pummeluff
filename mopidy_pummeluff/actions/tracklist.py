'''
Python module for Mopidy Pummeluff tracklist tag.
'''

__all__ = (
    'Tracklist',
    'ToggleShuffle',
)

from logging import getLogger

from .base import Action

LOGGER = getLogger(__name__)


class Tracklist(Action):
    '''
    Replace the tracklist with the URI of the tag's parameter.
    '''

    @classmethod
    def execute(cls, core, uri):  # pylint: disable=arguments-differ
        '''
        Replace tracklist and play.

        :param mopidy.core.Core core: The mopidy core instance
        :param str uri: An URI for the tracklist replacement
        '''
        LOGGER.info('Replacing tracklist with URI "%s"', uri)

        playlists = [playlist.uri for playlist in core.playlists.as_list().get()]

        if uri in playlists:
            uris = [item.uri for item in core.playlists.get_items(uri).get()]
        else:
            uris = [uri]

        core.tracklist.clear()
        core.tracklist.add(uris=uris)
        core.playback.play()


class ToggleShuffle(Action):
    '''
    Toggle random mode.
    '''

    @classmethod
    def execute(cls, core):
        '''
        Toggle random mode.

        :param mopidy.core.Core core: The mopidy core instance
        '''

        shuffle = core.tracklist.get_random().get()
        shuffle = not shuffle
        core.tracklist.set_random(shuffle)

        LOGGER.info('Toggling shuffle mode [%s]', shuffle)
