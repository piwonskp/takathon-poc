import os

from lark.lark import Lark
from lark.indenter import Indenter

from takathon.tester.execution import TestResults, execute
from takathon.tester.execution.builtins import BUILTINS
from takathon.tester.parser.transformer import ParseTreeToAST


path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'takathon.lark')


class GrammarIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8


def parse(mod, fname, tests):
    test_results = TestResults()
    mod.__dict__.update(BUILTINS)
    parser = Lark(open(path),
                  parser='lalr',
                  postlex=GrammarIndenter(),
                  transformer=ParseTreeToAST(mod, test_results, fname)
    )

    tree = parser.parse(tests)
    execute(tree)

    return test_results.passed, test_results.errors
