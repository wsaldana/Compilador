from automata import State, Fragment, graph
from notations import Notations
from utils.printer import print_return
from utils.exceptions import BadInfix, InfixNotBalanced


class AFN:
    def __init__(self):
        self.to_postfix = Notations.to_postfix

    @print_return("Compile")
    def compile(self, infix):
        if infix.count(')') != infix.count('('):
            raise InfixNotBalanced()

        postfix = self.to_postfix(infix)
        postfix = list(postfix)[::-1]
        nfa_stack = []

        while postfix:
            try:
                c = postfix.pop()

                if c == '.':
                    frag1 = nfa_stack.pop()
                    frag2 = nfa_stack.pop()
                    frag2.accept.edges.append(frag1.start)
                    start = frag2.start
                    accept = frag1.accept

                elif c == '|':
                    frag1 = nfa_stack.pop()
                    frag2 = nfa_stack.pop()
                    accept = State()
                    start = State(edges=[frag2.start, frag1.start])
                    frag2.accept.edges.append(accept)
                    frag1.accept.edges.append(accept)

                elif c == '*':
                    frag = nfa_stack.pop()
                    accept = State()
                    start = State(edges=[frag.start, accept])
                    frag.accept.edges = [frag.start, accept]

                elif c == '+':
                    frag = nfa_stack.pop()
                    accept = State()
                    start = State(edges=[frag.start])
                    frag.accept.edges.append(frag.start)
                    frag.accept.edges.append(accept)

                elif c == '?':
                    frag = nfa_stack.pop()
                    accept = State()
                    start = State(edges=[frag.start, accept])
                    frag.start.edges.append(frag.accept)
                    frag.accept.edges.append(accept)

                else:
                    accept = State()
                    start = State(label=c, edges=[accept])

                newfrag = Fragment(start, accept)
                nfa_stack.append(newfrag)

            except Exception as err:
                raise BadInfix()

        return nfa_stack.pop()

    def followes(self, state, current):
        if state not in current:
            current.add(state)
            if state.label is None:
                for x in state.edges:
                    self.followes(x, current)

    @print_return("MATCH")
    def match(self, regex, s):
        nfa = self.compile(regex)
        current = set()
        self.followes(nfa.start, current)
        previous = set()

        for c in s:
            previous = current
            current = set()
            for state in previous:
                if state.label is not None:
                    if state.label == c:
                        self.followes(state.edges[0], current)

        return nfa.accept in current


if __name__ == "__main__":
    afn = AFN()
    regex = input("Please enter a regular expression: ")
    s = input("Please enter a string to match: ")
    afn.match(regex, s)
    graph.dot.view()
