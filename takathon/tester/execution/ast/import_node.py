from dataclasses import dataclass

from takathon.tester.execution.ast.tree import Node


@dataclass
class Import(Node):
    cmd : str

    def execute(self, local_scope):
        exec(self.cmd, self.module.__dict__, local_scope)
