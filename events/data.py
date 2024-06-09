import json
import os

def get_data_file():
    return os.path.join(os.path.dirname(__file__), 'events.json')

def read_json():
    with open(get_data_file(), 'r') as file:
        return json.load(file)

def write_json(data):
    with open(get_data_file(), 'w') as file:
        json.dump(data, file)
