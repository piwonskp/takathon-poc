from dataclasses import dataclass

from takathon.tester.execution import TestResults
from takathon.tester.execution.ast.tree import Node


@dataclass
class CallFun(Node):
    test_results : TestResults
    fname : str
    args : str

    def call_fun(self, local_scope):
        return eval(f'{self.fname}({self.args})',
                    self.module.__dict__, local_scope)
