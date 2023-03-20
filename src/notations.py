import graphviz


class Notations:
    def __init__(self, infix):
        self.infix = infix
        self.precedencia = {
            '*': 3,
            '+': 3,
            '?': 3,
            '.': 2,
            '|': 1,
            '(': 0,
            ')': 0,
            '': 0
        }

    def explicit_contact(self):
        infix = ""
        for i in range(len(self.infix)):
            chr = self.infix[i]
            infix += chr

            if i < (len(self.infix) - 1):
                if (
                    ((chr in ')*+?') or (chr not in '?+()*.|'))
                    and (self.infix[i + 1] not in '+*?|)')
                ):
                    infix += '.'
        return infix

    def to_postfix(self):
        infix = self.explicit_contact()
        postfix = ""
        stack = []

        for chr in infix:
            if (chr == '('):
                stack += chr
            elif (chr == ')'):
                while (not (len(stack) < 1) and stack[-1] != '('):
                    postfix += stack.pop()
                stack.pop()
            elif (chr in ['*', '.', '|', '+', '?']):
                while (not len(stack) < 1):
                    if self.precedencia[stack[-1]] >= self.precedencia[chr]:
                        postfix += stack.pop()
                    else:
                        break
                stack.append(chr)
            else:
                postfix += chr

        while (not (len(stack) < 1)):
            postfix += stack.pop()

        return postfix

    def get_alphabet(self, infix):
        alphabet = []
        for i in infix:
            if (i not in '().*+|$?' and i not in alphabet):
                alphabet.append(i)
        return sorted(alphabet)


class RegEx:
    """Class representing a regular expression"""
    def __init__(self, value):
        self.value = value

    def syntax_tree(self):
        if len(self.value) == 1:
            # Base case: single character
            return State(self.value, accepting=True)
        elif self.value.startswith('(') and self.value.endswith(')'):
            # Recursive case: expression in parentheses
            sub_expr = RegEx(self.value[1:-1])
            return sub_expr.syntax_tree()
        elif '|' in self.value:
            # Recursive case: alternation
            left_expr, right_expr = self.value.split('|', 1)
            left_sub_expr = RegEx(left_expr)
            right_sub_expr = RegEx(right_expr)
            left_state = left_sub_expr.syntax_tree()
            right_state = right_sub_expr.syntax_tree()
            start_state = State('start')
            end_state = State('end', accepting=True)
            start_state.add_transition('eps', left_state)
            start_state.add_transition('eps', right_state)
            left_state.add_transition('eps', end_state)
            right_state.add_transition('eps', end_state)
            return start_state
        else:
            # Recursive case: concatenation
            left_expr = RegEx(self.value[0])
            right_expr = RegEx(self.value[1:])
            left_state = left_expr.syntax_tree()
            right_state = right_expr.syntax_tree()
            left_state.add_transition(right_expr.value[0], right_state)
            return left_state

    def to_dfa(self):
        syntax_tree = self.syntax_tree()

        def build_state(state_set):
            name = ''.join(sorted(state_set))
            accepting = any(s.accepting for s in state_set)
            transitions = {}
            for symbol in set(s.transition_symbols() for s in state_set):
                target = syntax_tree.get_state(syntax_tree.step(state_set, symbol))
                transitions[symbol] = build_state(target)
            return State(name, accepting=accepting, transitions=transitions)

        start_state = build_state(syntax_tree.step(set([syntax_tree.start]), 'eps'))
        return DFA(start_state)


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def make_graph(self):
        dot = graphviz.Digraph()
        self._make_graph(dot, self)
        dot.render("renders/tree", format='png')
        return dot

    def _make_graph(self, dot, node):
        if node is None:
            return
        dot.node(str(node), str(node.value))
        if node.left is not None:
            dot.edge(str(node), str(node.left))
            self._make_graph(dot, node.left)
        if node.right is not None:
            dot.edge(str(node), str(node.right))
            self._make_graph(dot, node.right)


def build_tree(postfix):
    stack = []
    operators = {'*', '.', '|'}
    for char in postfix:
        if char in operators:
            right = stack.pop()
            left = None
            if len(stack) > 0:
                left = stack.pop()
            stack.append(Node(char, left, right))
        else:
            stack.append(Node(char))
    return stack.pop()


if __name__ == "__main__":
    postfix = 'ab|c*.'
    root = build_tree(postfix)
    dot = root.make_graph()
