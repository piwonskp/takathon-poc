import os, sys

from glob import iglob
from importlib import import_module

from takathon.lib.path_finder import TestModuleFinder
from takathon.lib.path_name_resolver import get_module_name
from takathon.lib.splitter import get_code_and_tests
from takathon.tester.parser import parse


def get_files(path):
    if os.path.isdir(path):
        path = os.path.join(path, '**', '*.taka')
        return iglob(path, recursive=True)
    return [path]


def make_modules_importable(splitted):
    modules = {path: code for path, (code, _) in splitted.items()}
    sys.meta_path.append(TestModuleFinder(modules))


separate_tests = lambda src: get_code_and_tests(open(src).read())
def get_module_tests(path):
    splitted = {path: separate_tests(path)
                for path in get_files(path)
                }
    make_modules_importable(splitted)

    return {import_module(get_module_name(path)): tests
            for path, (_, tests) in splitted.items()}


def test_files(path):
    passed, errors = 0, 0
    tests = get_module_tests(path)

    for mod, mod_tests in tests.items():
        for fname, ftest in mod_tests.items():
            fpassed, ferrors = parse(mod, fname, ftest)
            passed += fpassed
            errors += ferrors

    print('Testing finished! {} tests passed, {} errors'
          .format(passed, errors))
