from abc import ABC, abstractmethod

# Estrutura do Composite 
class Node(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self.parent: Node | None = None

    @abstractmethod
    def accept(self, visitor) -> object:
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.name}'>"

class CompositeNode(Node):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.children: list[Node] = []

    def add(self, node: Node) -> None:
        node.parent = self
        self.children.append(node)
        print(f"[Composite] Adicionado {node} em {self}")

    def remove(self, node: Node) -> None:
        node.parent = None
        self.children.remove(node)
        print(f"[Composite] Removido {node} de {self}")

    def accept(self, visitor) -> object:
        # O visitante pode decidir o que fazer com os nós compostos.
        return visitor.visit_decision(self)

class DecisionNode(CompositeNode):
    pass

class LeafNode(Node):
    def __init__(self, name, payload: object | None = None) -> None:
        super().__init__(name)
        self.payload = payload

    def accept(self, visitor) -> object:
        return visitor.visit_leaf(self)
    
    
# Estrutura do Iterator
class PreOrderIterator:
    """Iterador pré-ordem (raiz, depois filhos da esquerda para a direita)."""   
    def __init__(self, root: Node) -> None:
        self.stack: list[Node] = []
        if root is not None:
            self.stack.append(root)

    def __iter__(self) -> "PreOrderIterator":
        return self

    def __next__(self) -> Node:
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
    def visit_decision(self, decision_node: DecisionNode) -> int | None:
        pass

    @abstractmethod
    def visit_leaf(self, leaf_node: LeafNode) -> int | None:
        pass

class DepthVisitor(Visitor):
    """Mockado: reporta profundidade da árvore."""
    def __init__(self) -> None:
        self._max_depth: int = 0

    def visit_decision(self, decision_node: DecisionNode) -> int:
        # Imprime e retorna um valor de profundidade fictício derivado do comprimento do nome do nó
        print(f"[Visitor:Depth] Visitando nó de decisão {decision_node.name}. (mock: calculando profundidade)")
        # Número simulado
        mocked_depth: int = len(decision_node.name) % 5 + 1 
        print(f"[Visitor:Depth] Profundidade (mock) para {decision_node.name}: {mocked_depth}")
        return mocked_depth

    def visit_leaf(self, leaf_node: LeafNode) -> int:
        print(f"[Visitor:Depth] Visitando folha {leaf_node.name}. (mock)" )
        mocked_depth: int = 1
        print(f"[Visitor:Depth] Profundidade (mock) para {leaf_node.name}: {mocked_depth}")
        return mocked_depth

class CountLeavesVisitor(Visitor):
    """Mockado: conta folhas via iteração e também faz prints representativos."""
    def __init__(self) -> None:
        self.count: int = 0

    def visit_decision(self, decision_node: DecisionNode) -> None:
        print(f"[Visitor:CountLeaves] Visitando nó de decisão {decision_node.name} (mock)." )
        # mock: não altera a contagem
        return None

    def visit_leaf(self, leaf_node: LeafNode) -> int:
        self.count += 1
        print(f"[Visitor:CountLeaves] Encontrada folha {leaf_node.name}. Total (mock): {self.count}")
        return self.count
    
    
# Estrutura do State (TreeBuilder)
class TreeBuilderState(ABC):
    def __init__(self, builder: "TreeBuilder") -> None:
        self.builder = builder

    @abstractmethod
    def handle(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} para {self.builder.name}>"

class SplittingState(TreeBuilderState):
    def handle(self) -> None:
        print(f"[State] {self.builder.name}: entrando em SplittingState (mock)." )
        # mock: cria dois nós filhos sob o alvo atual
        target: Node = self.builder.current_target or self.builder.root
        left: DecisionNode = DecisionNode(f"split_left_of_{target.name}")
        right: LeafNode = LeafNode(f"split_right_of_{target.name}")
        target.add(left)
        target.add(right)
        print(f"[State] {self.builder.name}: divisão mock realizada em {target}.")

class StoppingState(TreeBuilderState):
    def handle(self) -> None:
        print(f"[State] {self.builder.name}: entrando em StoppingState (mock)." )
        target: Node = self.builder.current_target or self.builder.root
        leaf: LeafNode = LeafNode(f"stopped_leaf_of_{target.name}")
        target.add(leaf)
        print(f"[State] {self.builder.name}: parada mock realizada em {target}.")

class PruningState(TreeBuilderState):
    def handle(self) -> None:
        print(f"[State] {self.builder.name}: entrando em PruningState (mock)." )
        target: Node = self.builder.current_target or self.builder.root
        # mock: remove o último filho se existir
        if isinstance(target, CompositeNode) and target.children:
            removed: Node = target.children[-1]
            target.remove(removed)
            print(f"[State] {self.builder.name}: poda mock removeu {removed} de {target}.")
        else:
            print(f"[State] {self.builder.name}: nada a podar em {target}.")

class TreeBuilder:
    def __init__(self, name: str, root: CompositeNode | None = None) -> None:
        self.name = name
        self.root = root or DecisionNode("root")
        self.current_target: Node = self.root
        # instanciando estados
        self.splitting: SplittingState = SplittingState(self)
        self.stopping: StoppingState = StoppingState(self)
        self.pruning: PruningState = PruningState(self)
        self.state: TreeBuilderState = self.splitting
        print(f"[TreeBuilder] Criado TreeBuilder '{self.name}' com root {self.root}")

    def set_target(self, node: Node) -> None:
        self.current_target = node
        print(f"[TreeBuilder] Target atual definido para {node}")

    def set_state(self, state_name: str) -> None:
        mapping: dict[str, TreeBuilderState] = {
            'splitting': self.splitting,
            'stopping': self.stopping,
            'pruning': self.pruning
        }
        self.state = mapping.get(state_name, self.state)
        print(f"[TreeBuilder] Estado alterado para {self.state}")

    def handle(self) -> None:
        print(f"[TreeBuilder] {self.name}: handle() chamado no estado {self.state}")
        self.state.handle()