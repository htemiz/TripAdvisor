import json

with open('settings.json') as setting_file:
    settings = json.load(setting_file)

    print('hotelsteyiz')
    print(settings)


__all__ = ['get_Albums', 'settings']


# from . users import *

