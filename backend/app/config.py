import os
import yaml


class Configuration:
    def __init__(self):
        self.config = None
        self.load_config()

    def load_config(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(root_dir, '..', 'configuration', 'app_config.yml')
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def get_config(self, key):
        return self.config.get(key, None)
