'''
Python module for Mopidy Pummeluff base action.
'''

__all__ = (
    'Action',
)

from logging import getLogger
from inspect import getfullargspec

LOGGER = getLogger(__name__)


class Action:
    '''
    Base RFID tag class, which will implement the factory pattern in Python's
    own :py:meth:`__new__` method.
    '''

    @classmethod
    def execute(cls, core):
        '''
        Execute the action.

        :param mopidy.core.Core core: The mopidy core instance

        :raises NotImplementedError: When class method is not implemented
        '''
        name  = cls.__name__
        error = 'Missing execute class method in the %s class'
        LOGGER.error(error, name)
        raise NotImplementedError(error % name)

    def __init__(self, uid, alias=None, parameter=None):
        '''
        Concstructor.
        '''
        self.uid       = uid
        self.alias     = alias
        self.parameter = parameter
        self.scanned   = None

    def __str__(self):
        '''
        String representation of tag.

        :return: The alias
        :rtype: str
        '''
        return self.alias or self.uid

    def __repr__(self):
        '''
        Instance representation of tag.

        :return: The class name and UID
        :rtype: str
        '''
        identifier = self.alias or self.uid
        return f'<{self.__class__.__name__} {identifier}>'

    def __call__(self, core):
        '''
        Action method which is called when the tag is detected on the RFID
        reader.

        :param mopidy.core.Core core: The mopidy core instance
        '''
        args = [core]
        if self.parameter:
            args.append(self.parameter)
        self.execute(*args)

    def as_dict(self, include_scanned=False):
        '''
        Dict representation of the tag.

        :param bool include_scanned: Include scanned timestamp

        :return: The dict version of the tag
        :rtype: dict
        '''
        data = {
            'action_class': self.__class__.__name__,
            'uid': self.uid,
            'alias': self.alias or '',
            'parameter': self.parameter or '',
        }

        if include_scanned:
            data['scanned'] = self.scanned

        return data

    def validate(self):
        '''
        Validate parameter.

        :raises ValueError: When parameter is not allowed but defined
        '''
        parameterised = len(getfullargspec(self.execute).args) > 2

        if parameterised and not self.parameter:
            raise ValueError('Parameter required for this tag')

        if not parameterised and self.parameter:
            raise ValueError('No parameter allowed for this tag')
