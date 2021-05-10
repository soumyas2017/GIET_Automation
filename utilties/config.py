import yaml
from functools import cache


def get_env(key=None):
    with open(r'D:\\configs\\config2.yaml') as file:
        vars = yaml.load(file, Loader=yaml.FullLoader)
        if key is None:
            return vars
        else:
            return vars[key]

