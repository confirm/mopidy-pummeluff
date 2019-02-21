# -*- coding: utf-8 -*-
'''
Mopidy Pummeluff Python module.
'''

from __future__ import absolute_import, unicode_literals

import os

from mopidy import config, ext

from .frontend import PummeluffFrontend
from .web import LatestHandler, RegistryHandler, RegisterHandler


def app_factory(config, core):
    return [
        ('/latest/', LatestHandler, {'core': core}),
        ('/registry/', RegistryHandler, {'core': core}),
        ('/register/', RegisterHandler, {'core': core}),
    ]


class Extension(ext.Extension):
    '''
    Mopidy Pummeluff extension.
    '''

    dist_name = 'Mopidy-Pummeluff'
    ext_name = 'pummeluff'

    def get_default_config(self):
        '''
        Return the default config.
        '''
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        '''
        Return the config schema.
        '''
        schema = super(Extension, self).get_config_schema()
        return schema

    def setup(self, registry):
        '''
        Setup the extension.
        '''
        registry.add('frontend', PummeluffFrontend)

        registry.add('http:static', {
            'name': self.ext_name,
            'path': os.path.join(os.path.dirname(__file__), 'webui'),
        })

        registry.add('http:app', {
            'name': self.ext_name,
            'factory': app_factory,
        })
