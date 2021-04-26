'''
CLI Interface of this extension.
'''

import logging

from mopidy import commands

from .registry import REGISTRY


logger = logging.getLogger(__name__)


class PummeluffCommand(commands.Command):
    '''
    Main Command class.
    '''
    def __init__(self):
        super().__init__()
        self.add_child("list", ListCommand())

    def run(self, args, config):
        pass


class ListCommand(commands.Command):
    '''
    Prints out the stored tags and their appropriate values on the terminal.
    '''
    def run(self, args, config):
        '''
        Prints out the stored tags and values on the terminal.
        '''

        for tag in REGISTRY.values():
            logger.info("%s -> %s",tag, tag.as_dict())

        return 0
