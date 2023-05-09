import graphviz
from src.automata import MyState, Transition, Automata


class Thompson():

    EPSILON = "ε"

    def __init__(
            self,
            postfix,
            alphabet
    ):
        """Crea una construccion de thompson con fragmentos de AFN

        Args:
            postfix (str): Postfix a representar en el automata
            alphabet (list): Caracteres que forman parte del alfabeto
        """
        self.postfix = postfix
        self.alphabet = alphabet
        self.n_states = 0
        self.states = set()
        self.afn = []

    def construct(self):
        skip = False
        for ch in self.postfix:
            if (ch == "'"):
                if skip:
                    skip = False
                else:
                    skip = True
            if (ch in self.alphabet and skip) or (ch in self.alphabet and ch not in 'д|*+?'):
                self.afn.append(self.label(ch))
            elif (ch == 'д'):
                a = self.afn.pop()
                b = self.afn.pop()
                self.afn.append(self.concat(b, a))
            elif (ch == '|'):
                a = self.afn.pop()
                b = self.afn.pop()
                self.afn.append(self.union(b, a))
            elif (ch == '*'):
                afn = self.afn.pop()
                self.afn.append(self.kleene(afn))
            elif (ch == '+'):
                afn = self.afn.pop()
                self.afn.append(self.kleene_plus(afn))
            elif (ch == '?'):
                afn = self.afn.pop()
                self.afn.append(self.qs(afn))

        self.afn[0].n_states = len(self.afn[0].states)
        self._afn = self.afn[0]
        return self.afn[0]

    def concat_fragments(self, transitions):
        new_afn = []
        for i in transitions:
            if type(i) is list:
                new_afn += self.concat_fragments(i)
            else:
                new_afn.append(i)
        return new_afn

    def label(self, label):
        self.n_states += 1
        state_i = MyState(self.n_states)
        self.n_states += 1
        state_f = MyState(self.n_states)
        t = self.concat_fragments(
            [Transition(state_i, label, state_f)]
        )
        self.states.add(state_i)
        self.states.add(state_f)
        return Automata(
            state_i,
            state_f,
            self.n_states,
            t,
            [state_i, state_f]
        )

    def union(self, a, b):
        self.n_states += 1
        state_i = MyState(self.n_states)
        self.n_states += 1
        state_f = MyState(self.n_states)
        t = self.concat_fragments([
            a.transitions,
            b.transitions,
            Transition(a.state_f, self.EPSILON, state_f),
            Transition(b.state_f, self.EPSILON, state_f),
            Transition(state_i, self.EPSILON, a.state_i),
            Transition(state_i, self.EPSILON, b.state_i)
        ])
        s = a.states + b.states
        s.append(state_i)
        s.append(state_f)
        for state in s:
            self.states.add(state)
        return Automata(state_i, state_f, self.n_states, t, s)

    def kleene(self, afn):
        self.n_states += 1
        state_i = MyState(self.n_states)
        self.n_states += 1
        state_f = MyState(self.n_states)
        t = self.concat_fragments([
            afn.transitions,
            Transition(afn.state_f, self.EPSILON, afn.state_i),
            Transition(state_i, self.EPSILON, afn.state_i),
            Transition(afn.state_f, self.EPSILON, state_f),
            Transition(state_i, self.EPSILON, state_f)
        ])
        s = afn.states
        s.append(state_i)
        s.append(state_f)
        for state in s:
            self.states.add(state)
        return Automata(state_i, state_f, self.n_states, t, s)

    def kleene_plus(self, afn):
        self.n_states += 1
        state_i = MyState(self.n_states)
        self.n_states += 1
        state_f = MyState(self.n_states)
        t = self.concat_fragments([
            afn.transitions,
            Transition(afn.state_f, self.EPSILON, afn.state_i),
            Transition(state_i, self.EPSILON, afn.state_i),
            Transition(afn.state_f, self.EPSILON, state_f),
        ])
        s = afn.states
        s.append(state_i)
        s.append(state_f)
        for state in s:
            self.states.add(state)
        return Automata(state_i, state_f, self.n_states, t, s)

    def qs(self, afn):
        self.n_states += 1
        state_i = MyState(self.n_states)
        self.n_states += 1
        state_f = MyState(self.n_states)
        t = self.concat_fragments([
            afn.transitions,
            Transition(state_i, self.EPSILON, afn.state_i),
            Transition(afn.state_f, self.EPSILON, state_f),
            Transition(state_i, self.EPSILON, state_f),
        ])
        states = afn.states
        states.append(state_i)
        states.append(state_f)
        for state in states:
            self.states.add(state)
        states = afn.states
        return Automata(state_i, state_f, self.n_states, t, states)

    def concat(self, a, b):
        for t in b.transitions:
            if (t.state_i == b.state_i):
                t.state_i = a.state_f
            elif (t.state_f == b.state_i):
                t.state_f == a.state_f
        b.states.remove(b.state_i)
        states = a.states + b.states
        state_i = a.state_i
        state_f = b.state_f
        t = self.concat_fragments([a.transitions, b.transitions])
        return Automata(state_i, state_f, self.n_states, t, states)

    def intersection(self, l1, l2):
        return [
            value
            for value
            in l1
            if value in l2
        ]

    def move(self, states, label):
        states_new = []
        stack = []

        if (not type(states) is list):
            stack.append(states)
        else:
            for i in states:
                stack.append(i)

        while len(stack) > 0:
            t = stack.pop()
            for trans in self._afn.transitions:
                if trans.state_i == t and trans.label == label:
                    if trans.state_f not in states_new:
                        states_new.append(trans.state_f)
        return states_new

    def e_closure(self, states):
        e = []
        stack = []

        for i in states:
            stack.append(i)
            e.append(i)

        while len(stack) != 0:
            t = stack.pop()
            for trans in self._afn.transitions:
                if trans.state_i == t and trans.label == self.EPSILON:
                    if trans.state_f not in e:
                        e.append(trans.state_f)
                        stack.append(trans.state_f)
        return e

    def simulate(self, string):
        state_f = [self._afn.state_f]
        S = self.e_closure([self._afn.state_i])
        rev = list(string)
        rev.reverse()

        while len(rev) > 0:
            S = self.e_closure(self.move(S, rev.pop()))

        if (self.intersection(S, state_f) != []):
            return "Si"
        else:
            return "No"

    def graph(self, nfa):
        g = graphviz.Digraph(comment="AFN")
        g.attr(rankdir='LR')
        for state in nfa.states:
            if state == nfa.state_i:
                g.edge('start', str(state))
                g.node('start', shape='point')
                g.node(str(state), shape='circle', style='bold')
            elif state == nfa.state_f:
                g.node(str(state), shape='doublecircle')
            else:
                g.node(str(state), shape='circle')

        for transicion in nfa.transitions:
            origen, simbolo, destino = transicion.state_i, transicion.label, transicion.state_f
            g.edge(str(origen), str(destino), label=str(simbolo))
        g.render("renders/AFN", format='png')
