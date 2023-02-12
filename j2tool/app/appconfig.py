from copy import deepcopy
import os
from typing import Any
import yaml

from j2tool.cross.singleton import SingletonMeta


class ConfigManager(metaclass=SingletonMeta):
    def __init__(self, config=None):
        self.config_file = ""
        self.config = {"verbose": 0, "no_color": False}
        if config:
            self.config = config

    def load(self, filepath):
        with open(filepath, encoding="utf-8") as file:
            options = yaml.load(file, Loader=yaml.FullLoader)
            self.config.update(options)

    def load_folder_config(self, dir):
        config_path = os.path.join(dir, "j2r.config")
        result = {}
        if os.path.exists(config_path):
            with open(config_path, encoding="utf-8") as file:
                result = yaml.load(file, Loader=yaml.FullLoader)

        return result

    def get_config_value(self, key: str) -> Any:
        return self.config.get(key, None)

    def set_config_value(self, key, value):
        self.config[key] = value

    def get_config(self):
        return deepcopy(self.config)
