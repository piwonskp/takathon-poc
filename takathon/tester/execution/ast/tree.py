from dataclasses import dataclass
from types import ModuleType

from lark import Tree


class ASTTree(Tree):
    def execute(self, local_scope):
        for node in self.children:
            node.execute(local_scope)


@dataclass
class Node:
    module : ModuleType
