'''
Mopidy Pummeluff Python module.
'''

import os

import mopidy
import pkg_resources

from .frontend import PummeluffFrontend
from .web import ActionsHandler, LatestHandler, RegisterHandler, RegistryHandler, UnregisterHandler

__version__ = pkg_resources.get_distribution('Mopidy-Pummeluff').version


def app_factory(config, core):  # pylint: disable=unused-argument
    '''
    App factory for the web apps.

    :param mopidy.config config: The mopidy config
    :param mopidy.core.Core core: The mopidy core

    :return: The registered app request handlers
    :rtype: list
    '''
    return [
        ('/latest/', LatestHandler),
        ('/registry/', RegistryHandler),
        ('/register/', RegisterHandler),
        ('/unregister/', UnregisterHandler),
        ('/actions/', ActionsHandler),
    ]


class Extension(mopidy.ext.Extension):
    '''
    Mopidy Pummeluff extension.
    '''

    dist_name = 'Mopidy-Pummeluff'
    ext_name = 'pummeluff'
    version = __version__

    def get_default_config(self):  # pylint: disable=no-self-use
        '''
        Return the default config.

        :return: The default config
        :rtype: str
        '''
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return mopidy.config.read(conf_file)

    def get_config_schema(self):
        '''
        Return the config schema.

        :return: The config schema
        :rtype: mopidy.config.schemas.ConfigSchema
        '''
        schema = super().get_config_schema()
        for pin in ('led', 'shutdown', 'play_pause', 'stop', 'previous_track', 'next_track'):
            schema[f'{pin}_pin'] = mopidy.config.Integer()

        return schema

    def setup(self, registry):
        '''
        Setup the extension.

        :param mopidy.ext.Registry registry: The mopidy registry
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
