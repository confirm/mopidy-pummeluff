'''
Python module for Mopidy Pummeluff web classes.
'''

__all__ = (
    'LatestHandler',
    'RegistryHandler',
    'RegisterHandler',
    'UnregisterHandler',
    'ActionClassesHandler',
)

from json import dumps
from logging import getLogger

from tornado.web import RequestHandler

from mopidy_pummeluff.registry import REGISTRY
from mopidy_pummeluff.actions import ACTIONS
from mopidy_pummeluff.threads import TagReader

LOGGER = getLogger(__name__)


class LatestHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which returns the latest scanned tag.
    '''

    def get(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle GET request.
        '''
        tag = TagReader.latest

        LOGGER.debug('Returning latest tag %s', tag)

        if tag is None:
            data = {
                'success': False,
                'message': 'No tag scanned yet'
            }

        else:
            data = {
                'success': True,
                'message': 'Scanned tag found',
            }

            data.update(tag.as_dict(include_scanned=True))

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))


class RegistryHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which returns all registered tags.
    '''

    def get(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle GET request.
        '''
        tags_list = []

        for tag in REGISTRY.values():
            tags_list.append(tag.as_dict())

        data = {
            'success': True,
            'message': 'Registry successfully read',
            'tags': tags_list
        }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))


class RegisterHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which registers an RFID tag in the registry.
    '''

    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle POST request.
        '''
        try:
            tag = REGISTRY.register(
                action_class=self.get_argument('action-class'),
                uid=self.get_argument('uid'),
                alias=self.get_argument('alias', None),
                parameter=self.get_argument('parameter', None),
            )

            data = {
                'success': True,
                'message': 'Tag successfully registered',
            }

            data.update(tag.as_dict())

        except ValueError as ex:
            self.set_status(400)
            data = {
                'success': False,
                'message': str(ex)
            }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))

    def put(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle PUT request.
        '''
        self.post()


class UnregisterHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which unregisters an RFID tag from the registry.
    '''

    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle POST request.
        '''
        try:
            REGISTRY.unregister(uid=self.get_argument('uid'))

            data = {
                'success': True,
                'message': 'Tag successfully unregistered',
            }

        except ValueError as ex:
            self.set_status(400)
            data = {
                'success': False,
                'message': str(ex)
            }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))

    def put(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle PUT request.
        '''
        self.post()


class ActionClassesHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which returns all action classes.
    '''

    def get(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle GET request.
        '''
        data = {
            'success': True,
            'message': 'Action classes successfully retreived',
            'action_classes': ACTIONS
        }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))
