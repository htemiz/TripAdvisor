import json

with open('./settings.json') as setting_file:
    settings = json.load(setting_file)


__all__ = ['open_page']


from . utils import *

