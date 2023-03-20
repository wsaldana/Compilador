import graphviz
from src.afn import Transition, Automata


class Subconjuntos():

    EPSILON = 'ε'

    def __init__(
            self,
            afn,
            alphabet
    ):
        """Algoritmo de creacion de AFD por medio de subconjuntos.
        Referencias del libro del dragón.

        Args:
            AFN (Automata): AFN que se convertira a AFD
            alphabet (list): list del alfabeto aceptado
        """
        self.afn = afn
        self.alphabet = alphabet
        self.state_i = None
        self.state_f = []
        self.temp = []
        self.trans = []

    def construct(self):
        label_encoder = {}
        labels = [
            'Z', 'Y', 'X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N',
            'M', 'L', 'K', 'J', 'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
        states = [self.e_closure([self.afn.state_i])]
        visited = []
        while (not all(s in visited for s in states)):
            for s in states:
                visited.append(s)
                for label in self.alphabet:
                    U = self.e_closure(self.move(s, label))
                    if U not in states:
                        states.append(U)
                    if s != []:
                        if U != []:
                            self.temp.append(Transition(s, label, U))
        for s in visited:
            if s != []:
                name = labels.pop()
                label_encoder[name] = s

        for trans in self.temp:
            new_state_i, new_state_f = None, None
            for key, value in label_encoder.items():
                if value == trans.state_i:
                    new_state_i = key
                if value == trans.state_f:
                    new_state_f = key
            self.trans.append(
                Transition(new_state_i, trans.label, new_state_f)
            )

        for key, values in label_encoder.items():
            if self.afn.state_i in values:
                self.state_i = key
            if self.afn.state_f in values:
                self.state_f.append(key)
        self.afd = Automata(
            self.state_i,
            self.state_f,
            len(label_encoder),
            self.trans,
            list(label_encoder.keys())
        )
        return self.afd

    def move(self, states, label, v=False):
        new_states = []
        stack = []
        if (not type(states) is list):
            stack.append(states)
        else:
            for i in states:
                stack.append(i)
        trs = self.afd.transitions if v else self.afn.transitions
        while len(stack) > 0:
            t = stack.pop()
            for trans in trs:
                if (trans.state_i == t and trans.label == label):
                    if (trans.state_f not in new_states):
                        new_states.append(trans.state_f)
        return new_states

    def e_closure(self, states):
        res = []
        stack = []

        for i in states:
            stack.append(i)
            res.append(i)

        while (len(stack) != 0):
            t = stack.pop()
            for trans in self.afn.transitions:
                if (trans.state_i == t and trans.label == self.EPSILON):
                    if (trans.state_f not in res):
                        res.append(trans.state_f)
                        stack.append(trans.state_f)
        return res

    def simulate(self, string):
        current_s = self.afd.state_i
        for i in string:
            current_s = self.move(current_s, i, True)
            if (current_s is None):
                return None
        if (current_s[0] in self.afd.state_f):
            return "Si"
        else:
            return "No"

    def graph(self, dfa):
        g = graphviz.Digraph(comment="AFD")
        g.attr(rankdir='LR')
        for state in dfa.states:
            if state == dfa.state_i:
                g.edge('start', str(state))
                g.node('start', shape='point')
                g.node(str(state), shape='circle', style='bold')
            elif state in dfa.state_f:
                g.node(str(state), shape='doublecircle')
            else:
                g.node(str(state), shape='circle')
        for transicion in dfa.transitions:
            origen, simbolo, destino = transicion.state_i, transicion.label, transicion.state_f
            g.edge(str(origen), str(destino), label=str(simbolo))
        g.render("renders/AFD", format='png')
