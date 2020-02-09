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
        self.action.__func__(*args)

    @property
    def action(self):
        '''
        Return an action function defined in the
        :py:mod:`mopidy_pummeluff.actions` Python module.

        :return: An action
        :raises NotImplementedError: When action property isn't defined
        '''
        cls   = self.__class__.__name__
        error = 'Missing action property in the %s class'
        LOGGER.error(error, cls)
        raise NotImplementedError(error % cls)

    def as_dict(self, include_scanned=False):
        '''
        Dict representation of the tag.

        :param bool include_scanned: Include scanned timestamp

        :return: The dict version of the tag
        :rtype: dict
        '''
        data = {
            'tag_class': self.__class__.__name__,
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
        if self.parameterised and not self.parameter:
            raise ValueError('Parameter required for this tag')

        if not self.parameterised and self.parameter:
            raise ValueError('No parameter allowed for this tag')
