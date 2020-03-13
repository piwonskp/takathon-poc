import re
from dataclasses import dataclass
from types import ModuleType

from lark import Transformer, Tree

from takathon.tester.execution import TestResults
from takathon.tester.execution.ast import ASTTree, Domain, MockNode, Import
from takathon.tester.execution.ast.result_validators import CheckResult, CheckThrow, CheckByFunction


def transform_mock(module, tree):
    new_tree = []
    for node in reversed(tree):
        if type(node) == Tree:
            mo = re.match(r'mock (?P<target>.*?) as (?P<val>.*)', node.children[0])
            new_tree = [MockNode(mo.group('target'), mo.group('val'),
                                 module, new_tree)]
        else:
            new_tree.insert(0, node)
    return new_tree


def get_expected_result(token):
    return re.match(r'results (?P<res>.+)', token).group('res')


def get_result_validator(token):
    return re.match(r'result (?P<validator>.+)', token).group('validator')


def map_keywords_to_function_name(args):
    return re.sub('any of', 'any_of', args)


def get_args(tokens):
    return re.match(r'domain (?P<args>.*):', tokens.pop(0)).group('args')


@dataclass
class ParseTreeToAST(Transformer):
    module : ModuleType
    test_results : TestResults
    function_name : str

    def start(self, tokens):
        return ASTTree('root', transform_mock(self.module, tokens))

    def import_stmt(self, tokens):
        return Import(self.module, tokens[0].value)

    def domain_stmt(self, tokens):
        args = map_keywords_to_function_name(get_args(tokens))
        make_result_validator = tokens[-1]
        tokens[-1] = make_result_validator(args)

        tree = transform_mock(self.module, tokens)
        return Domain('test_scope', tree)

    def fun_call(self, tokens):
        token = tokens[0]
        if token.type == 'RESULTS_STMT':
            return self.result_validator(CheckResult,
                                         get_expected_result(token))
        elif token.type == 'RESULT_BY_FUNCTION_STMT':
            return self.result_validator(CheckByFunction,
                                         get_result_validator(token))
        else:
            expected_exc = re.match(r'throws (?P<exc>.+)', token).group('exc')
            return self.result_validator(CheckThrow, expected_exc)

    def result_validator(self, cls, pass_condition):
        return lambda args: cls(self.module, self.test_results,
                                self.function_name, args,
                                pass_condition)
