import json

with open('config/configuration.json') as setting_file:
    configuration = json.load(setting_file)

__all__ = ['configuration']
