# Projeto: Árvore de Decisão (Mock)
- **Autor:** Samuel Corrêa Lima
- **Disciplina:** Engenharia de Software

## Padrões de Projeto Utilizados
Este projeto faz uso de quatro padrões de projeto clássicos da Engenharia de Software:

- **Composite:** Permite representar a árvore como uma estrutura hierárquica, onde nós compostos e nós folhas são tratados de maneira uniforme. Implementado com Node, CompositeNode, LeafNode e DecisionNode.
- **Iterator:** Define um modo de percorrer a árvore sem expor sua estrutura interna. Implementado com PreOrderIterator, que faz a travessia em pré-ordem.
- **Visitor:** Permite adicionar operações sobre os nós sem modificar suas classes. Implementado com Visitor, DepthVisitor e CountLeavesVisitor.
- **State:** Permite alterar o comportamento do construtor da árvore dinamicamente, dependendo do estado atual. Implementado com TreeBuilder e os estados SplittingState, StoppingState e PruningState.

## Diagramas de Classes
Todos os diagramas apresentados foram desenvolvidos de acordo com o padrão UML, utilizando a ferramenta **PlantUML** para sua modelagem e representação gráfica.

### Composite (Node, DecisionNode, LeafNode)
<img width="630" height="527" alt="image" src="https://github.com/user-attachments/assets/d86eaf3f-c0ff-48df-bcb6-beeba7e73f19" />

### Visitor (DepthVisitor, CountLeavesVisitor)
<img width="912" height="322" alt="image" src="https://github.com/user-attachments/assets/1376bedd-f855-4d11-9362-a43516867b17" />

### Iterator (PreOrderIterator)
<img width="621" height="444" alt="image" src="https://github.com/user-attachments/assets/f01cb907-6bc0-46cc-95d0-8eeef429760c" />

### State (TreeBuilder + States)
<img width="576" height="612" alt="image" src="https://github.com/user-attachments/assets/f2934276-2ffe-4ddf-b423-942383e1b7fc" />

### Arquitetura Final (todos os padrões juntos)
<img width="1317" height="832" alt="image" src="https://github.com/user-attachments/assets/ed0d228e-d892-499b-afcd-a3e28135a553" />

## Arquivos
1. ``tree_design.py``: Estrutura dos padrões de projeto.
2. ``tree_demo.py``: Arquivo que demonstra o uso do design e executa operações via
prints.

## Como Rodar o Projeto
**Execute o arquivo ``tree_demo.py``**
```
python tree_demo.py
```
**Exemplo de saída esperada:**
```
====== Construindo árvore de exemplo ======
[Composite] Adicionado <DecisionNode 'LeftDecision'> em <DecisionNode 'RootDecision'>
[Composite] Adicionado <DecisionNode 'RightDecision'> em <DecisionNode 'RootDecision'>
[Composite] Adicionado <LeafNode 'LeafA'> em <DecisionNode 'LeftDecision'>
[Composite] Adicionado <LeafNode 'LeafB'> em <DecisionNode 'LeftDecision'>
[Composite] Adicionado <LeafNode 'LeafC'> em <DecisionNode 'RightDecision'>

====== Demo: TreeBuilder com estados (mock) ======
[TreeBuilder] Criado TreeBuilder 'MockBuilder' com root <DecisionNode 'root'>
[TreeBuilder] Estado alterado para <SplittingState para MockBuilder>
[TreeBuilder] MockBuilder: handle() chamado no estado <SplittingState para MockBuilder>
[State] MockBuilder: entrando em SplittingState (mock).
...
====== Demo finalizado ======
```


