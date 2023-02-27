class State:
    def __init__(self, label=None, edges=[]):
        self.edges = edges
        self.label = label

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
