from functools import partial

from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import log

import yaml

DEFAULT_FILE_PATH = 'regex_convert.txt'

info = partial(log.info, f'{__name__} %s')

class ObsidianSupportPlugin(BasePlugin):
    """
    mkdocs plugin that convert based on regular expression
    """

    config_scheme = (("file", config_options.Type(str, default=DEFAULT_FILE_PATH)))

    def on_config(self, config: MkDocsConfig):
        info(f'Configuring: {self.config}')

        filepath = config.get('file')

        with open(filepath) as f :
            regexpairs = yaml.load(f, Loader=yaml.FullLoader)
            print(regexpairs)