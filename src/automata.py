import graphviz


class Graph:
    def __init__(self) -> None:
        self.i = -1
        self.dot = graphviz.Digraph(format='png')
        self.dot.attr(rankdir='LR', size='20')
        self.dot.attr('node', shape='circle')

    def gid(self):
        self.i += 1
        return str(self.i)


graph = Graph()


class State:
    def __init__(self, label=None, edges=[]):
        self.edges = edges
        self.label = label

        i = graph.gid()
        graph.dot.node(i)
        for e in edges:
            label = e.label if e.label else 'ε'
            graph.dot.edge(i, graph.gid(), label)

    def __str__(self) -> str:
        label = self.label if self.label else 'ε'
        return f'({label}): {str(self.edges)}'

    def __repr__(self) -> str:
        return str(self)


class Fragment:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

    def __repr__(self) -> str:
        return f'Start: {str(self.start)} - Aceptacion: {str(self.accept)}'
