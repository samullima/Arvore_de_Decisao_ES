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
    
# Estrutura do Iterator
class PreOrderIterator:
    """Iterador pré-ordem (raiz, depois filhos da esquerda para a direita)."""   
    def __init__(self, root):
        self.stack = []
        if root is not None:
            self.stack.append(root)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration
        # LIFO: o último adicionado é o próximo a ser visitado
        node = self.stack.pop()  
        # A children mais à esquerda é a primeira a ser processada
        if isinstance(node, CompositeNode):
            for child in reversed(node.children):
                self.stack.append(child)
        return node
    
# Estrutura do Visitor 
class Visitor(ABC):
    @abstractmethod
    def visit_decision(self, decision_node):
        pass

    @abstractmethod
    def visit_leaf(self, leaf_node):
        pass

class DepthVisitor(Visitor):
    """Mockado: reporta profundidade da árvore."""
    def __init__(self):
        self._max_depth = 0

    def visit_decision(self, decision_node):
        # Imprime e retorna um valor de profundidade fictício derivado do comprimento do nome do nó
        print(f"[Visitor:Depth] Visitando nó de decisão {decision_node.name}. (mock: calculando profundidade)")
        # Número simulado
        mocked_depth = len(decision_node.name) % 5 + 1 
        print(f"[Visitor:Depth] Profundidade (mock) para {decision_node.name}: {mocked_depth}")
        return mocked_depth

    def visit_leaf(self, leaf_node):
        print(f"[Visitor:Depth] Visitando folha {leaf_node.name}. (mock)" )
        mocked_depth = 1
        print(f"[Visitor:Depth] Profundidade (mock) para {leaf_node.name}: {mocked_depth}")
        return mocked_depth

class CountLeavesVisitor(Visitor):
    """Mockado: conta folhas via iteração porém também faz prints representativos."""
    def __init__(self):
        self.count = 0

    def visit_decision(self, decision_node):
        print(f"[Visitor:CountLeaves] Visitando nó de decisão {decision_node.name} (mock)." )
        # mock: não altera a contagem
        return None

    def visit_leaf(self, leaf_node):
        self.count += 1
        print(f"[Visitor:CountLeaves] Encontrada folha {leaf_node.name}. Total (mock): {self.count}")
        return self.count