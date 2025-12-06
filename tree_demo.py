from tree_design import DecisionNode, LeafNode, TreeBuilder, PreOrderIterator, DepthVisitor, CountLeavesVisitor

# Demonstração do uso do design

def build_sample_tree():
    """
    Constrói e retorna uma árvore de exemplo usando DecisionNode e LeafNode.

    A estrutura criada segue o padrão Composite.

    Returns
    -------
    DecisionNode
        Nó raiz da árvore construída.
    """
    print("\n====== Construindo árvore de exemplo ======")
    root = DecisionNode("RootDecision")
    left = DecisionNode("LeftDecision")
    right = DecisionNode("RightDecision")
    leaf_a = LeafNode("LeafA")
    leaf_b = LeafNode("LeafB")
    leaf_c = LeafNode("LeafC")

    root.add(left)
    root.add(right)
    left.add(leaf_a)
    left.add(leaf_b)
    right.add(leaf_c)

    return root

def demo_builder():
    """
    Demonstra o uso do TreeBuilder e seus estados (Splitting, Stopping, Pruning).

    A função executa uma sequência mockada de operações para ilustrar o
    funcionamento do padrão State aplicado à construção e modificação de
    uma árvore de decisão. As etapas realizadas são:

    1. Criação de um TreeBuilder chamado "MockBuilder".
    2. Alteração do estado para 'splitting' e execução de uma divisão
       mock no nó raiz, adicionando dois filhos.
    3. Definição do primeiro filho como alvo e mudança para o estado
       'stopping', adicionando uma folha mock naquele ponto.
    4. Retorno do alvo para a raiz e mudança para o estado 'pruning',
       removendo um filho mock (caso exista).
    """
    print("\n====== Demo: TreeBuilder com estados (mock) ======")
    builder = TreeBuilder("MockBuilder")
    # Fazendo divisão mock no root
    builder.set_state('splitting')
    # Criando dois nós filhos mock
    builder.handle()  
    # Mudando target para o primeiro filho
    first_child = builder.root.children[0]
    builder.set_target(first_child)
    builder.set_state('stopping')
    # Adicionando uma folha mock
    builder.handle()  
    # Fazendo poda no root (mock)
    builder.set_target(builder.root)
    builder.set_state('pruning')
    builder.handle()
    
def demo_iterator_and_visitors(root):
    """
    Demonstra o uso do iterador em pré-ordem e dos visitantes (Visitors).

    A função percorre a árvore fornecida usando o `PreOrderIterator` e aplica
    dois visitantes mockados em cada nó.

    Parameters
    ----------
    root : Node
        Nó raiz da árvore que será percorrida em pré-ordem.
    """
    print("\n====== Demo: Iterator pré-ordem e Visitors (mock) ======")
    it = PreOrderIterator(root)
    depth_visitor = DepthVisitor()
    count_visitor = CountLeavesVisitor()
    print("Iterando nós e aplicando visitantes:")
    for node in it:
        print(f" - visitando nó: {node}")
        # Informações de teste de visitors
        node.accept(depth_visitor)
        # Contagem de folhas
        node.accept(count_visitor)  

    print(f"[Resultado mock] Contagem final de folhas (mock): {count_visitor.count}")

def main():
    # Constrói árvore de exemplo
    root = build_sample_tree()
    # Executa a demonstração do TreeBuilder
    demo_builder()
    # Executa a demonstração do iterador pré-ordem e dos visitantes
    demo_iterator_and_visitors(root)
    print("\n====== Demo finalizado ======\n")

if __name__ == "__main__":
    main()
 