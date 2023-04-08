import graphviz


class Notations:
    def __init__(self, infix):
        self.infix = infix
        self.precedencia = {
            '*': 3,
            '+': 3,
            '?': 3,
            'ю': 3,
            'д': 1,
            '|': 2,
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
                    ((chr in ')*+?') or (chr not in "?+()*д|\\'"))
                    and (self.infix[i + 1] not in "+*?|)'")
                ):
                    infix += 'д'
        return infix

    def to_postfix(self):
        infix = self.explicit_contact()
        postfix = ""
        stack = []
        skip_op = False

        for chr in infix:
            if (chr == '(') and not skip_op:
                stack += chr
            elif (chr == ')') and not skip_op:
                while (not (len(stack) < 1) and stack[-1] != '('):
                    postfix += stack.pop()
                stack.pop()
            elif (chr in ['*', 'д', '|', '+', '?', 'ю']) and not skip_op:
                while (not len(stack) < 1):
                    if self.precedencia[stack[-1]] >= self.precedencia[chr]:
                        postfix += stack.pop()
                    else:
                        break
                stack.append(chr)
            elif chr == "'":
                skip_op = not skip_op
            else:
                if skip_op:
                    postfix += f"'{chr}'"
                else:
                    postfix += chr

        while (not (len(stack) < 1)):
            postfix += stack.pop()

        return postfix

    def get_alphabet(self, infix):
        alphabet = []
        for i in infix:
            if (i not in '()д*+|$?ю' and i not in alphabet):
                alphabet.append(i)
        return sorted(alphabet)


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
    operators = ['*', 'д', '|', '+', '?', 'ю']
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
