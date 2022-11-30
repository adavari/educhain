import json
import os


class ConfigReader:

    def __init__(self):
        self.ROOT = os.getenv("BUILDER_ROOT")
        self.CONFIG = {}

    def read_config_file(self):
        with open(self.ROOT + '/config.json', 'r') as config_file:
            self.CONFIG = json.loads(config_file.read())

        return self.CONFIG