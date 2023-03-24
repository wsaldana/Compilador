import graphviz
from src.afn import Transition, Automata
from src.automata import MyState


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

    def graph(self, dfa, export_name='AFD'):
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
        g.render(f"renders/{export_name}", format='png')


class RegEx:
    def __init__(self, value):
        self.value = value

    def to_dfa(self, syntax_tree):
        def build_state(state_set):
            name = ''.join(sorted(state_set))
            accepting = any(s.accepting for s in state_set)
            transitions = {}
            for symbol in set(s.transition_symbols() for s in state_set):
                target = syntax_tree.get_state(
                    syntax_tree.step(state_set, symbol)
                )
                transitions[symbol] = build_state(target)
            return MyState(name, accepting=accepting, transitions=transitions)

        start_state = build_state(
            syntax_tree.step(set([syntax_tree.start]), ' ɛ')
        )
        return Automata(start_state)


def minimize_dfa(dfa):
    final_states = set(dfa.state_f)
    non_final_states = set(dfa.states) - final_states
    partitions = [final_states, non_final_states]
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    while True:
        new_partitions = []
        for partition in partitions:
            new_sub_partitions = {}
            for state in partition:
                transition_symbols = set(t.label for t in dfa.transitions if t.state_i == state)
                sub_partition_key = tuple(sorted([p for p in partitions if p & transition_symbols], key=lambda x: id(x)))
                if sub_partition_key not in new_sub_partitions:
                    new_sub_partitions[sub_partition_key] = set()
                new_sub_partitions[sub_partition_key].add(state)
            new_partitions.extend(new_sub_partitions.values())
        if new_partitions == partitions:
            break
        partitions = new_partitions

    state_map = {}
    new_states = []
    new_initial_state = None
    new_final_states = set()
    for i, partition in enumerate(partitions):
        new_state_name = letters[i]
        new_states.append(new_state_name)
        for state in partition:
            state_map[state] = new_state_name
            if state == dfa.state_i:
                new_initial_state = new_state_name
            if state in dfa.state_f:
                new_final_states.add(new_state_name)
    new_transitions = []
    print("Particiones: ", partitions)
    for partition in partitions:
        for label in set(t.label for t in dfa.transitions):
            transition_map = {}
            for state in partition:
                for transition in dfa.transitions:
                    if transition.state_i == state and transition.label == label:
                        transition_map[state_map[transition.state_f]] = True
            if transition_map:
                new_transitions.append(
                    Transition(
                        next(iter(partition)),
                        label,
                        next(iter(transition_map)),
                    )
                )

    return Automata(
        new_initial_state,
        new_final_states,
        len(new_states),
        new_transitions,
        new_states,
    )
