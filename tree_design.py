from abc import ABC, abstractmethod

# Estrutura do Composite 
class Node(ABC):
    """
    Classe base abstrata para todos os nós da árvore.

    Cada nó possui um nome e uma referência opcional ao seu nó pai.
    Subclasses devem implementar o método `accept` para permitir
    a aplicação do padrão Visitor.
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.parent: Node | None = None

    @abstractmethod
    def accept(self, visitor) -> object:
        """
        Aceita um visitante e passa a ele a operação apropriada.

        Args:
            visitor: Objeto que implementa a interface Visitor.

        Returns:
            object: Valor retornado pelo método de visita do visitante.
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.name}'>"

class CompositeNode(Node):
    """
    Representa um nó composto, que pode conter nós filhos.

    Essa classe implementa parte fundamental do padrão Composite,
    permitindo adicionar e remover nós, além de armazenar seus filhos.
    """
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.children: list[Node] = []

    def add(self, node: Node) -> None:
        """
        Adiciona um nó filho ao nó composto.

        Args:
            node: Instância de Node que será adicionada como filha.
        """
        node.parent = self
        self.children.append(node)
        print(f"[Composite] Adicionado {node} em {self}")

    def remove(self, node: Node) -> None:
        """
        Remove um nó filho do nó composto.

        Args:
            node: Instância de Node que será removida.
        """
        node.parent = None
        self.children.remove(node)
        print(f"[Composite] Removido {node} de {self}")

    def accept(self, visitor) -> object:
        """
        Aplica o visitante a um nó composto, chamando visit_decision.

        Args:
            visitor: Objeto que implementa a interface Visitor.

        Returns:
            object: Resultado de visitor.visit_decision(self).
        """
        # O visitante pode decidir o que fazer com os nós compostos.
        return visitor.visit_decision(self)

class DecisionNode(CompositeNode):
    """
    Nó de decisão, semanticamente igual a CompositeNode.

    Serve apenas para diferenciar decisões de outros nós compostos.
    """
    pass

class LeafNode(Node):
    """
    Representa um nó folha, sem filhos.

    Args:
        name: Nome do nó.
        payload: Dados associados à folha (opcional).
    """
    def __init__(self, name, payload: object | None = None) -> None:
        super().__init__(name)
        self.payload = payload

    def accept(self, visitor) -> object:
        """
        Aplica o visitante a uma folha, chamando visit_leaf.

        Args:
            visitor: Objeto que implementa a interface Visitor.

        Returns:
            object: Resultado de visitor.visit_leaf(self).
        """
        return visitor.visit_leaf(self)
    
    
# Estrutura do Iterator
class PreOrderIterator:
    """Iterador para percorrer a árvore em ordem pré-ordem.

    A iteração segue a ordem:
    1. Visita o nó atual (raiz da subárvore)
    2. Visita recursivamente cada um dos filhos da esquerda para a direita

    Este iterador utiliza uma pilha (stack) para realizar a travessia
    de forma iterativa.
    """ 
    def __init__(self, root: Node) -> None:
        """
        Inicializa o iterador com o nó raiz da árvore.

        Args:
            root: Nó inicial a partir do qual a travessia começa.
        """
        self.stack: list[Node] = []
        if root is not None:
            self.stack.append(root)

    def __iter__(self) -> "PreOrderIterator":
        """
        Retorna o próprio iterador.

        Returns:
            PreOrderIterator: instância do iterador.
        """
        return self

    def __next__(self) -> Node:
        """
        Retorna o próximo nó na travessia pré-ordem.

        A lógica funciona assim:
        - Remove o nó do topo da pilha (LIFO).
        - Se o nó for composto, seus filhos são empilhados na ordem inversa,
          garantindo que o filho mais à esquerda seja processado primeiro.

        Returns:
            Node: próximo nó da árvore na ordem pré-ordem.
        """
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
    """
    Define as operações que podem ser aplicadas a diferentes tipos de nós
    da árvore (DecisionNode e LeafNode). Cada novo visitante deve implementar
    esses métodos para definir seu próprio comportamento.
    """
    @abstractmethod
    def visit_decision(self, decision_node: DecisionNode) -> int | None:
        """
        Visita um nó de decisão.

        Args:
            decision_node: Instância de DecisionNode a ser processada.

        Returns:
            int | None: Resultado definido pelo visitante.
        """
        pass

    @abstractmethod
    def visit_leaf(self, leaf_node: LeafNode) -> int | None:
        """
        Visita um nó folha.

        Args:
            leaf_node: Instância de LeafNode a ser processada.

        Returns:
            int | None: Resultado definido pelo visitante.
        """
        pass

class DepthVisitor(Visitor):
    """
    Visitante que calcula uma profundidade mockada para cada nó.

    Este visitante não calcula profundidade real, ele gera valores fictícios
    baseados no comprimento do nome do nó.
    """
    def __init__(self) -> None:
        """Inicializa o visitante com profundidade máxima igual a zero."""
        self._max_depth: int = 0

    def visit_decision(self, decision_node: DecisionNode) -> int:
        """
        Processa um nó de decisão e retorna sua profundidade mockada.

        A profundidade é simulada usando:
        ``len(nome_do_no) % 5 + 1``

        Args:
            decision_node: O nó de decisão visitado.

        Returns:
            int: profundidade mockada calculada.
        """
        print(f"[Visitor:Depth] Visitando nó de decisão {decision_node.name}. (mock: calculando profundidade)")
        # Número simulado
        mocked_depth: int = len(decision_node.name) % 5 + 1 
        print(f"[Visitor:Depth] Profundidade (mock) para {decision_node.name}: {mocked_depth}")
        return mocked_depth

    def visit_leaf(self, leaf_node: LeafNode) -> int:
        """
        Processa um nó folha e retorna profundidade mockada.

        Como folhas sempre têm profundidade mínima, retorna sempre 1.

        Args:
            leaf_node: O nó folha visitado.

        Returns:
            int: profundidade mockada (sempre 1).
        """
        print(f"[Visitor:Depth] Visitando folha {leaf_node.name}. (mock)" )
        mocked_depth: int = 1
        print(f"[Visitor:Depth] Profundidade (mock) para {leaf_node.name}: {mocked_depth}")
        return mocked_depth

class CountLeavesVisitor(Visitor):
    """
    Visitante que conta o número de folhas encontradas.

    Cada vez que uma LeafNode é visitada, o contador interno é incrementado.
    """
    def __init__(self) -> None:
        """Inicializa o contador de folhas com zero."""
        self.count: int = 0

    def visit_decision(self, decision_node: DecisionNode) -> None:
        """
        Processa um nó de decisão.

        Neste visitante, nós de decisão não contribuem na contagem.

        Args:
            decision_node: O nó de decisão visitado.

        Returns:
            None
        """
        print(f"[Visitor:CountLeaves] Visitando nó de decisão {decision_node.name} (mock)." )
        return None

    def visit_leaf(self, leaf_node: LeafNode) -> int:
        """
        Processa um nó folha e incrementa a contagem interna.

        Args:
            leaf_node: O nó folha visitado.

        Returns:
            int: Quantidade total de folhas encontradas até o momento.
        """
        self.count += 1
        print(f"[Visitor:CountLeaves] Encontrada folha {leaf_node.name}. Total (mock): {self.count}")
        return self.count
    
    
# Estrutura do State (TreeBuilder)
class TreeBuilderState(ABC):
    """
    Classe base abstrata para estados do TreeBuilder.
    
    Cada estado representa uma etapa ou comportamento específico durante a
    construção dinâmica da árvore (ex.: divisão, parada ou poda).
    """
    def __init__(self, builder: "TreeBuilder") -> None:
        """
        Inicializa o estado com referência ao TreeBuilder controlador.

        Parameters
        ----------
        builder : TreeBuilder
            Objeto responsável por manter a árvore e manipular estados.
        """
        self.builder = builder

    @abstractmethod
    def handle(self) -> None:
        """Executa a ação associada ao estado específico."""
        pass

    def __repr__(self) -> str:
        """Retorna representação curta do estado, associando-o ao TreeBuilder."""
        return f"<{self.__class__.__name__} para {self.builder.name}>"

class SplittingState(TreeBuilderState):
    """
    Estado responsável por executar uma operação de divisão (split) no nó alvo.
    
    Esta versão é mockada: cria dois novos filhos (um DecisionNode e um LeafNode)
    sob o nó atualmente selecionado no TreeBuilder.
    """
    def handle(self) -> None:
        """Realiza a ação de divisão mock adicionando dois novos nós ao alvo."""
        print(f"[State] {self.builder.name}: entrando em SplittingState (mock)." )
        target: Node = self.builder.current_target or self.builder.root
        left: DecisionNode = DecisionNode(f"split_left_of_{target.name}")
        right: LeafNode = LeafNode(f"split_right_of_{target.name}")
        target.add(left)
        target.add(right)
        print(f"[State] {self.builder.name}: divisão mock realizada em {target}.")

class StoppingState(TreeBuilderState):
    """
    Estado responsável por marcar o encerramento de uma expansão na árvore.
    
    Esta implementação mockada adiciona uma folha ao nó alvo,
    representando o fim do crescimento naquele ponto.
    """
    def handle(self) -> None:
        """Realiza a ação mock de parada adicionando uma LeafNode ao alvo."""
        print(f"[State] {self.builder.name}: entrando em StoppingState (mock)." )
        target: Node = self.builder.current_target or self.builder.root
        leaf: LeafNode = LeafNode(f"stopped_leaf_of_{target.name}")
        target.add(leaf)
        print(f"[State] {self.builder.name}: parada mock realizada em {target}.")

class PruningState(TreeBuilderState):
    """
    Estado responsável por simular uma poda (pruning) da árvore.
    
    Esta versão mock remove o último filho do CompositeNode alvo, caso exista.
    """
    def handle(self) -> None:
        """Executa a ação de poda mock removendo o último filho do alvo."""
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
    """
    Controlador responsável por construir e manipular uma árvore de decisão
    utilizando o padrão State.

    O TreeBuilder possui um nó raiz, mantém o nó-alvo atual e alterna entre
    diferentes estados (splitting, stopping, pruning), delegando a eles as
    operações realizadas via `handle()`.
    """
    def __init__(self, name: str, root: CompositeNode | None = None) -> None:
        """
        Inicializa o TreeBuilder criando estados e definindo o nó raiz.

        Parameters
        ----------
        name : str
            Nome identificador do processo/construtor.
        root : CompositeNode | None, optional
            Nó raiz da árvore, se não fornecido, cria um DecisionNode padrão.
        """
        self.name = name
        self.root = root or DecisionNode("root")
        self.current_target: Node = self.root
        # Instanciando estados
        self.splitting: SplittingState = SplittingState(self)
        self.stopping: StoppingState = StoppingState(self)
        self.pruning: PruningState = PruningState(self)
        self.state: TreeBuilderState = self.splitting
        print(f"[TreeBuilder] Criado TreeBuilder '{self.name}' com root {self.root}")

    def set_target(self, node: Node) -> None:
        """
        Define o nó que será afetado pelo próximo estado.

        Parameters
        ----------
        node : Node
            Nó a ser considerado como alvo das operações futuras.
        """
        self.current_target = node
        print(f"[TreeBuilder] Target atual definido para {node}")

    def set_state(self, state_name: str) -> None:
        """
        Altera o estado ativo do TreeBuilder com base no nome fornecido.

        Parameters
        ----------
        state_name : str
            Nome do estado desejado: 'splitting', 'stopping' ou 'pruning'.
        """
        mapping: dict[str, TreeBuilderState] = {
            'splitting': self.splitting,
            'stopping': self.stopping,
            'pruning': self.pruning
        }
        self.state = mapping.get(state_name, self.state)
        print(f"[TreeBuilder] Estado alterado para {self.state}")

    def handle(self) -> None:
        """Executa a operação associada ao estado atual."""
        print(f"[TreeBuilder] {self.name}: handle() chamado no estado {self.state}")
        self.state.handle()