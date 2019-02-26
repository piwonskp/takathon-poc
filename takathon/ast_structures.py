from unittest.mock import patch

from lark import Tree

from unittest.mock import Mock

DEFAULT_LOCALS = {
    'Mock': Mock,
}


SUCCESS = 0
ERROR = 1


class TestResults:
    passed = 0
    errors = 0


def execute(tree, mod, fun):
    return tree.execute(mod, fun, dict(DEFAULT_LOCALS))


class ASTTree(Tree):
    def execute(self, module, fn, local_scope):
        for node in self.children:
            node.execute(module, fn, local_scope)


class MockNode(ASTTree):
    def __init__(self, name, value, *args, **kwargs):
        super().__init__('mock_node', *args, **kwargs)
        self.name, self.value = name, value

    def execute(self, module, fn, local_scope):
        value = eval(self.value, module.__dict__, local_scope)

        path = (self.name[1:] if self.name.startswith('`')
                else '{}.{}'.format(module.__name__, self.name)
                )
        with patch(path, value):
            super().execute(module, fn, local_scope)

class Import:
    def __init__(self, cmd):
        self.cmd = cmd

    def execute(self, module, fn, local_scope):
        exec(self.cmd, local_scope)


class CallFun:
    def __init__(self, test_results, args=None):
        self.test_results = test_results
        self.args = args

    def call_fun(self, mod, fn):
        cmd = '{}({})'.format(fn, self.args)

        return eval(cmd, mod.__dict__)


class CheckResult(CallFun):
    def __init__(self, expected_result, *args, **kwargs):
        self.expected_result = expected_result
        super().__init__(*args, **kwargs)

    def execute(self, module, fn, local_scope):
        result = self.call_fun(module, fn)
        expected_result = eval(self.expected_result,
                               module.__dict__, local_scope)

        try:
            assert result == expected_result
            self.test_results.passed += 1
        except AssertionError:
            self.test_results.errors += 1
            print('Error in function {} domain {}: Expected {} got {}'
                  .format(fn, self.args, expected_result, result))


class CheckThrow(CallFun):
    def __init__(self, expected_exc, *args, **kwargs):
        self.expected_exc = expected_exc
        super().__init__(*args, **kwargs)

    def execute(self, module, fn, local_scope):
        try:
            self.call_fun(module, fn)
        except Exception as e:
            expected = eval(self.expected_exc, module.__dict__)
            if type(expected) == type:
                expected = expected()

            try:
                assert (type(e) is type(expected)
                        and e.args == expected.args)

                self.test_results.passed += 1
            except AssertionError:
                self.test_results.errors +=1
                print('''Wrong exception in function {} domain {}:
                Expected {} got {}'''
                      .format(fn, self.args, type(expected), type(e)))
        else:
            self.test_results.errors +=1
            print('''Error in function {} domain {}:
            Expected exception {}. No exception has been raised
            '''.format(fn, self.args, self.expected_exc)
            )
