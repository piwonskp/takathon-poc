import re
import os

from functools import reduce

from lark import Transformer, Tree
from lark.lark import Lark
from lark.indenter import Indenter
from lark.tree import Visitor

from takathon.ast_structures import ASTTree, TestResults, MockNode, Import, CheckResult, CheckThrow, execute


path = os.path.join(os.path.dirname(__file__), 'takathon.g')


class GrammarIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8


def transform_mock(tree):
    new_tree = []
    for node in reversed(tree):
        if type(node) == Tree:
            mo = re.match('mock (?P<target>.*?) as (?P<val>.*)', node.children[0])
            new_tree = [MockNode(mo.group('target'), mo.group('val'), new_tree)]
        else:
            new_tree.insert(0, node)
    return new_tree


class ParseTreeToAST(Transformer):
    def __init__(self, test_results, *args, **kwargs):
        self.test_results = test_results
        super().__init__(*args, **kwargs)

    def start(self, tokens):
        return ASTTree('root', transform_mock(tokens))

    def import_stmt(self, tokens):
        return Import(tokens[0].value)

    def domain_stmt(self, tokens):
        args = re.match(r'domain (?P<args>.*):', tokens.pop(0)).group('args')
        tokens[-1].args = args

        tree = transform_mock(tokens)
        return ASTTree('test_scope', tree)

    def fun_call(self, tokens):
        token = tokens[0]
        if token.type == 'RESULTS_STMT':
            expected_result = re.match(r'results (?P<res>.+)', token).group('res')
            return CheckResult(expected_result, self.test_results)
        else:
            expected_exc = re.match(r'throws (?P<exc>.+)', token).group('exc')
            return CheckThrow(expected_exc, self.test_results)


def parse(mod, fun, tests):
    test_results = TestResults()
    parser = Lark(open(path),
                  parser='lalr',
                  postlex=GrammarIndenter(),
                  transformer=ParseTreeToAST(test_results)
    )

    tree = parser.parse(tests)
    execute(tree, mod, fun)

    return test_results.passed, test_results.errors
