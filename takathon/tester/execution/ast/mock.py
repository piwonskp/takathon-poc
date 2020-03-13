from unittest.mock import patch

from takathon.tester.execution.ast.tree import ASTTree
from takathon.tester.execution.ast.tree import Node


class MockNode(Node, ASTTree):
    def __init__(self, name, value, module, *args, **kwargs):
        super().__init__(module)
        ASTTree.__init__(self, 'mock_node', *args, **kwargs)
        self.name, self.value = name, value

    def execute(self, local_scope):
        value = eval(self.value, self.module.__dict__, local_scope)

        path = (self.name[1:] if self.name.startswith('`')
                else '{}.{}'.format(self.module.__name__, self.name)
                )
        with patch(path, value):
            super().execute(local_scope)
