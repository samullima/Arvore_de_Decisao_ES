from abc import ABC, abstractmethod

# Estrutura do Composite 
class Node(ABC):
    def __init__(self, name):
        self.name = name
        self.parent = None

    @abstractmethod
    def accept(self, visitor):
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.name}'>"

class CompositeNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def add(self, node):
        node.parent = self
        self.children.append(node)
        print(f"[Composite] Adicionado {node} em {self}")

    def remove(self, node):
        node.parent = None
        self.children.remove(node)
        print(f"[Composite] Removido {node} de {self}")

    def accept(self, visitor):
        # O visitante pode decidir o que fazer com os nós compostos.
        return visitor.visit_decision(self)

class DecisionNode(CompositeNode):
    pass

class LeafNode(Node):
    def __init__(self, name, payload=None):
        super().__init__(name)
        self.payload = payload

    def accept(self, visitor):
        return visitor.visit_leaf(self)
