'''
Python module for Mopidy Pummeluff volume tag.
'''

__all__ = (
    'Volume',
)

from mopidy_pummeluff.actions import set_volume
from .base import Tag


class Volume(Tag):
    '''
    Sets the volume to the percentage value retreived from the tag's parameter.
    '''

    action = set_volume

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
