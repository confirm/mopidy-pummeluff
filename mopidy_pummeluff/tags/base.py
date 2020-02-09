'''
Python module for Mopidy Pummeluff base tag.
'''

__all__ = (
    'Tag',
)

from logging import getLogger

LOGGER = getLogger(__name__)


class Tag:
    '''
    Base RFID tag class, which will implement the factory pattern in Python's
    own :py:meth:`__new__` method.
    '''
    parameterised = True

    def __init__(self, uid, alias=None, parameter=None):
        '''
        Concstructor.
        '''
        self.uid       = uid
        self.alias     = alias
        self.parameter = parameter

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
        self.action.__func__(*args)

    @property
    def dict(self):
        '''
        Dict representation of the tag.
        '''
        return {
            'tag_class': self.__class__.__name__,
            'uid': self.uid,
            'alias': self.alias or '',
            'parameter': self.parameter or ''
        }

    @property
    def action(self):
        '''
        Return a name of an action (function) defined in the
        :py:mod:`mopidy_pummeluff.actions` Python module.

        :return: An action name
        :rtype: str
        :raises NotImplementedError: When action property isn't defined
        '''
        cls   = self.__class__.__name__
        error = 'Missing action property in the %s class'
        LOGGER.error(error, cls)
        raise NotImplementedError(error % cls)

    def validate(self):
        '''
        Validate parameter.

        :raises ValueError: When parameter is not allowed but defined
        '''
        if self.parameterised and not self.parameter:
            raise ValueError('Parameter required for this tag')

        if not self.parameterised and self.parameter:
            raise ValueError('No parameter allowed for this tag')
