from takathon.tester.execution.ast import ASTTree


class Domain(ASTTree):
    def execute(self, local_scope):
        local_scope = {}
        super().execute(local_scope)
