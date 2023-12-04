import json


def update(json, path, new_value,):
    obj_ptr = json
    for key in path:
        if key == path[-1]:
            obj_ptr[key] = new_value
        obj_ptr = obj_ptr[key]

    return obj_ptr
    # with open(file_path, 'w') as config_file:
    #     json.dump(obj_ptr, config_file)


def update_config(file_path='configuration.json', path=None, new_value=''):
    with open(file_path) as config_file:
        configuration = json.load(config_file)

        update(configuration, path, new_value)

    with open(file_path, 'w') as config_file:
        json.dump(configuration, config_file)

