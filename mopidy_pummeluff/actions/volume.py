'''
Python module for Mopidy Pummeluff volume tag.
'''

__all__ = (
    'Volume',
)

from logging import getLogger

from .base import Action

LOGGER = getLogger(__name__)


class Volume(Action):
    '''
    Sets the volume to the percentage value retreived from the tag's parameter.
    '''

    @classmethod
    def execute(cls, core, volume):  # pylint: disable=arguments-differ
        '''
        Set volume of the mixer.

        :param mopidy.core.Core core: The mopidy core instance
        :param volume: The new (percentage) volume
        :type volume: int|str
        '''
        LOGGER.info('Setting volume to %s', volume)
        try:
            core.mixer.set_volume(int(volume))
        except ValueError as ex:
            LOGGER.error(str(ex))

    def validate(self):
        '''
        Validates if the parameter is an integer between 0 and 100.

        :param mixed parameter: The parameter

        :raises ValueError: When parameter is invalid
        '''
        super().validate()

        try:
            number = int(self.parameter)
            assert 0 <= number <= 100
        except (ValueError, AssertionError):
            raise ValueError('Volume parameter has to be a number between 0 and 100')
