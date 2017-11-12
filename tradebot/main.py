"""Main module"""


import logging
import sys
from .config import AppConfig
from .input import Commandline, read_commandline_args
from .logging import setup_logging


def main():
    """Module entrypoint"""
    args = read_commandline_args()
    config = AppConfig(**args)
    config.load()
    setup_logging(
        log=config.get('log'),
        loglevel=config.get('loglevel')
    )
    log = logging.getLogger(__name__)
    log.debug('Configuration loaded: %s', config._config)

    app = MainApp(config)

    while True:
        action = app.get_action()
        if action == 'quit':
            sys.stdout.write('\n')
            log.debug('Application exited')
            break
        else:
            app.run_action(action)


class MainApp(object):
    """Main application state"""

    def __init__(self, config):
        self.config = config
        self.log = logging.getLogger(__name__)
        self.cmd = Commandline(self.config)

    def get_action(self):
        """Get an action to run"""
        action = self.config.get('action')
        if action:
            # Read first action from command line and then remove it
            del self.config['action']
        else:
            action = self.cmd.prompt()

        return action

    def run_action(self, action):
        """Run an action"""
        print(action)
