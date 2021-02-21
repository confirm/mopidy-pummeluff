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
    Replaces the current tracklist with the URI retreived from the tag's
    parameter.
    '''

    @classmethod
    def _browse_uri(cls, core, uri):
        '''
        Searches all tracks in uri (if it is a directory) and sub directories.

        :param mopidy.core.Core core: The mopidy core instance
        :param str uri: the URI
        '''
        # try to browse it - maybe it is a directory
        uris = []
        for ref in core.library.browse(uri).get():
            if ref.type == ref.TRACK:
                uris.append(ref.uri)
            elif ref.type == ref.DIRECTORY:
                uris.extend(cls._browse_uri(core, ref.uri))
        return uris

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
            # if uri points to a Directory, we have to call browse to get all
            # the Tracks. Right now it is not possible to get the type of an
            # URI. So we just try to browse uri and if it is not a directory
            # this will return an empty list of uris.
            uris = cls._browse_uri(core, uri)
            if not uris:
                # browse failed
                uris = [uri]

        LOGGER.info('uris: %s', uris)

        core.tracklist.clear()
        core.tracklist.add(uris=uris)
        core.playback.play()


class ToggleShuffle(Action):
    '''
    Toggles random mode
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
