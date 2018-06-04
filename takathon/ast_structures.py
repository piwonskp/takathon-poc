from unittest.mock import patch

from lark import Tree

from takathon import default_locals


SUCCESS = 0
ERROR = 1


class TestResults:
    passed = 0
    errors = 0



class ASTTree(Tree):
    def execute(self, module, fn):
        for node in self.children:
            node.execute(module, fn)


class MockNode(ASTTree):
    def __init__(self, name, value, *args, **kwargs):
        super().__init__('mock_node', *args, **kwargs)
        self.name, self.value = name, value

    def execute(self, module, fn):
        value = eval(self.value, module.__dict__, default_locals.__dict__)

        path = (self.name[1:] if self.name.startswith('`')
                else '{}.{}'.format(module.__name__, self.name)
                )
        with patch(path, value):
            super().execute(module,fn)

class Import:
    def __init__(self, cmd):
        self.cmd = cmd

    def execute(self, module, fn):
        exec(self.cmd, default_locals.__dict__)

class CheckResult:
    def __init__(self, args, expected_result, test_results):
        self.args = args
        self.expected_result = expected_result
        self.test_results = test_results

    def execute(self, module, fn):
        cmd = '{}({})'.format(fn, self.args)
        scope = module.__dict__

        result = eval(cmd, scope)
        expected_result = eval(self.expected_result, scope)

        try:
            assert result == expected_result
            self.test_results.passed += 1
        except AssertionError:
            print('Error function {} domain {}: Expected {} got {}'
                  .format(fn, self.args, expected_result, result))
            self.test_results.errors += 1
