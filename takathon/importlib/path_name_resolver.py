import os

from pathlib import PurePath


def get_path(module_name):
    splitted = module_name.split('.')
    path = os.path.join(*splitted)
    if os.path.isdir(path):
        return os.path.join(path, '__init__.taka'), True

    return path + '.taka', False


def get_module_name(path):
    path, _ = os.path.splitext(path)
    if os.path.basename(path) == '__init__':
        path = os.path.dirname(path)

    return '.'.join(PurePath(path).parts)
