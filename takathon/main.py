import os, sys, types

from glob import iglob
from importlib import import_module
from importlib.util import spec_from_loader, module_from_spec

from takathon.path_finder import TestModuleFinder, TestModuleLoader
from takathon.path_name_resolver import get_module_name
from takathon.splitter import get_code_and_tests
from takathon.parser import parse

def get_files(path):
    if os.path.isdir(path):
        path = os.path.join(path, '**', '*.taka')
        return iglob(path, recursive=True)
    return [path]


def test_files(path):
    separate_tests = lambda src: get_code_and_tests(open(src).read())
    splitted = {path: separate_tests(path)
                for path in get_files(path)
                }
    modules = {path: code for path, (code, _) in splitted.items()}
    sys.meta_path.append(TestModuleFinder(modules))

    tests = {import_module(get_module_name(path)): tests
             for path, (_, tests) in splitted.items()}

    passed, errors = 0, 0

    for mod, mod_tests in tests.items():
        for fname, ftest in mod_tests.items():
            fpassed, ferrors = parse(mod, fname, ftest)
            passed += fpassed
            errors += ferrors

    print('Testing finished! {} tests passed, {} errors'
          .format(passed, errors))
