import re


MATCH_TESTS = 'test (?P<func_name>.+)\((?P<args>.*)\):\n(?P<test>[\s\S]+)\ndef:'

def _fun_name(matchobj):
    fname = matchobj.group('func_name')
    args = matchobj.group('args')
    return f'def {fname}({args}):'


def get_code(module):
    return re.sub(MATCH_TESTS, _fun_name, module)


def get_code_and_tests(module):
    tests = {}

    def add_function_tests(matchobj):
        tests[matchobj.group('func_name')] = 'test:\n' + matchobj.group('test')
        return _fun_name(matchobj)

    mod = re.sub(MATCH_TESTS, add_function_tests, module)

    return mod, tests
