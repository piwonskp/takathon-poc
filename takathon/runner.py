import sys

from takathon.lib.path_finder import TestModuleFinder
from takathon.lib.splitter import get_code


def run_file(file, argv):
    sys.argv = (file.name, ) + argv
    sys.meta_path.append(TestModuleFinder())
    exec(get_code(file.read()), {'__name__': '__main__'})
