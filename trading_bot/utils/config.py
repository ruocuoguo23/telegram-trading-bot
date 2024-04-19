import os
import yaml


class TelegramConfig:
    def __init__(self, token=None):
        self.token = token


class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.telegram_config = TelegramConfig()

        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            return

        with open(self.config_path, 'r') as stream:
            try:
                cfg = yaml.safe_load(stream)
                if 'telegram' in cfg:
                    self.telegram_config.token = cfg['telegram']['token']
            except yaml.YAMLError as exc:
                print(exc)
