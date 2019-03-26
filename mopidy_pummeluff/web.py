# -*- coding: utf-8 -*-
'''
Python module for Mopidy Pummeluff web classes.
'''

from __future__ import absolute_import, unicode_literals

__all__ = (
    'LatestHandler',
    'RegistryHandler',
    'RegisterHandler',
)

from json import dumps
from logging import getLogger

from tornado.web import RequestHandler

from . import tags
from .threads import TagReader

LOGGER = getLogger(__name__)


class LatestHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which returns the latest scanned tag.
    '''

    def initialize(self, core):  # pylint: disable=arguments-differ
        '''
        Initialize request handler with Mopidy core.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        self.core = core

    def get(self, *args, **kwargs):
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

            data.update(tag.dict)

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))


class RegistryHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which returns all registered tags.
    '''

    def initialize(self, core):  # pylint: disable=arguments-differ
        '''
        Initialize request handler with Mopidy core.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        self.core = core

    def get(self, *args, **kwargs):
        '''
        Handle GET request.
        '''
        tags_list = []

        for tag in tags.Tag.all().values():
            tags_list.append(tag.dict)

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

    def initialize(self, core):  # pylint: disable=arguments-differ
        '''
        Initialize request handler with Mopidy core.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        self.core = core

    def post(self, *args, **kwargs):
        '''
        Handle POST request.
        '''
        try:
            tag = tags.Tag.register(
                uid=self.get_argument('uid'),
                alias=self.get_argument('alias', None),
                parameter=self.get_argument('parameter'),
                tag_type=self.get_argument('type')
            )

            data = {
                'success': True,
                'message': 'Tag successfully registered',
            }

            data.update(tag.dict)

        except ValueError as ex:
            self.set_status(400)
            data = {
                'success': False,
                'message': str(ex)
            }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))

    def put(self, *args, **kwargs):
        '''
        Handle PUT request.
        '''
        self.post()


class TypesHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which returns all tag types.
    '''

    def initialize(self, core):  # pylint: disable=arguments-differ
        '''
        Initialize request handler with Mopidy core.

        :param mopidy.core.Core mopidy_core: The mopidy core instance
        '''
        self.core = core

    def get(self, *args, **kwargs):
        '''
        Handle GET request.
        '''
        types = {}

        for cls_name in tags.__all__:
            tag_cls = getattr(tags, cls_name)
            if tag_cls is not tags.Tag:
                tag_type        = tags.Tag.get_type(tag_cls)
                tag_doc         = tag_cls.__doc__.strip().split('.')[0]
                types[tag_type] = tag_doc

        data = {
            'success': True,
            'message': 'Types successfully retreived',
            'types': types
        }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))
