import json


def get_fixture_data(path):
    """Opening a json file for tests."""
    with open(path, 'r') as f:
        data = json.load(f)
        return data
