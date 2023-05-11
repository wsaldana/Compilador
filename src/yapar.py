from utils.exceptions import YaparSyntaxError
import graphviz
import uuid


class Grammar:
    def __init__(self, label='0'):
        self.non_terminals = []
        self.label = label

    def __getitem__(self, key):
        for nt in self.non_terminals:
            if nt.label == key:
                return nt

    def extend(self):
        nt = self.non_terminals[0]
        new_nt = NonTerminal("S'")
        new_nt.productions.append(nt.label)
        self.non_terminals.insert(0, new_nt)

    def shift_closure(self, prod):
        lst = prod.split()
        if '.' not in lst:
            lst.insert(0, '.')
            return lst

        i = lst.index('.')
        del lst[i]
        lst.insert(i+1, '.')
        return lst

    def closure(self):
        i = 0
        for nt in self.non_terminals:
            j = 0
            for prod in nt.productions:
                tks = self.shift_closure(prod)
                self.non_terminals[i].productions[j] = ' '.join(tks)
                j += 1
            i += 1

    def append(self, non_terminal):
        self.non_terminals.append(non_terminal)

    def last(self):
        return self.non_terminals[-1]

    def __repr__(self) -> str:
        string = ''
        for nt in self.non_terminals:
            string += str(nt) + '\n'
        return string

    def __str__(self) -> str:
        return self.__repr__()

    def keys(self):
        return [nt.label for nt in self.non_terminals]


class NonTerminal:
    def __init__(self, label):
        self.label = label
        self.productions = []

    def __eq__(self, other) -> bool:
        return self.label == other.label

    def __repr__(self) -> str:
        return f'{self.label} -> {" | ".join(self.productions)}'

    def __str__(self) -> str:
        return self.__repr__()


class Yapar:
    def __init__(self, yalex_tokens):
        self.tokens = []
        self.grammar = Grammar()
        self.ignored = []
        self.yalex_tokens = yalex_tokens

    def read(self, file_name):
        prods = False

        with open(file_name, 'r') as file:
            n_line = 0

            for line in file:
                n_line += 1

                if '%%' in line:
                    prods = True
                    continue

                if line.startswith("/*"):
                    continue

                if prods:
                    self.read_productions(line, n_line)
                else:
                    self.read_tokens(line, n_line)

    def read_tokens(self, line: str, n_line: int):
        words = line.split()

        if len(words) == 0:
            return

        if words[0] == '%token':
            self.tokens += words[1:]
        elif words[0] == 'IGNORE':
            self.ignored += words[1:]
        else:
            raise YaparSyntaxError(line=n_line)

    def read_productions(self, line: str, n_line: int):
        if len(line) == 1:
            return

        if ":" in line:
            nt = NonTerminal(line[:-1][0].upper())
            self.grammar.append(nt)
        elif ";" in line:
            pass
        else:
            line = line.replace("|", "")
            rule = ""
            current = self.grammar.last()
            for tk in line.split():
                if tk in self.yalex_tokens:
                    if len(self.yalex_tokens[tk]) == 1:
                        rule += " " + self.yalex_tokens[tk][0]
                    else:
                        rule += " " + tk.lower()
                else:
                    rule += " " + tk[0].upper()
            current.productions.append(rule[1:])

    def first(self, label):
        non_terminal = self.grammar[label]
        labels = self.grammar.keys()
        firsts = []
        for production in non_terminal.productions:
            tokens = production.split()
            if tokens[0] == label:
                continue
            elif tokens[0] in labels:
                firsts += self.first(tokens[0])
            else:
                firsts += [tokens[0]]
        return firsts

    def follow(self):
        labels = self.grammar.keys()
        follows = {k: set() for k in labels}
        follows[labels[0]].add('$')

        for nt in self.grammar.non_terminals:
            rules = nt.productions
            for rule in rules:
                tks = rule.split()
                if len(tks) == 3:
                    follows[nt.label].add(tks[1])
                elif len(tks) == 2:
                    follows[tks[1]] = follows[tks[1]].union(follows[nt.label])
                elif len(tks) == 1 and tks[0] in labels:
                    follows[tks[0]] = follows[tks[0]].union(follows[nt.label])
                elif len(tks) == 1 and tks[0] not in labels:
                    index = labels.index(nt.label)
                    label = labels[index - 1]
                    follows[label] = follows[label].union(follows[nt.label])
        return follows

    def shift_closure(self, prod):
        lst = prod.split()
        if '.' not in lst:
            lst.insert(0, '.')
            return lst

        i = lst.index('.')
        del lst[i]
        lst.insert(i+1, '.')
        return lst

    def closure(self, dot, grammar):
        done = []
        for nt in grammar.non_terminals:
            for prod in nt.productions:
                tks = prod.split()
                index = tks.index('.')
                if index == len(tks)-1:
                    pass
                else:
                    edge = tks[index + 1]
                    if edge in done:
                        continue
                    else:
                        done.append(edge)
                    item_collection = Grammar()
                    # Jalar las producciones que tengan edge (la produccion antes del punto) dentro
                    node_id = str(uuid.uuid4())
                    dot.node(node_id, label="x")
                    dot.edge(grammar.label, node_id, label=edge)
                    for nt in grammar.non_terminals:
                        for prod in nt.productions:
                            if edge in prod:
                                tks1 = self.shift_closure(prod)
                                new_nt = NonTerminal(label=nt.label)
                                new_nt.productions.append(' '.join(tks1))
                                item_collection.append(new_nt)
                    dot.node(node_id, label=str(item_collection))

    def build_lr0(self):
        dot = graphviz.Digraph()
        self.grammar.extend()
        self.grammar.closure()
        dot.node(self.grammar.label, label=str(self.grammar))
        self.closure(dot, self.grammar)
        dot.render("renders/lr0", format='png')


if __name__ == "__main__":
    tokens = {'WHITESPACE': ['\t', '\n', ' '], 'ID': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'], 'NUMBER': ['+', '-', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'E'], 'PLUS': ['+'], 'MINUS': ['-'], 'TIMES': ['*'], 'DIV': ['/'], 'LPAREN': ['('], 'RPAREN': [')']}
    y = Yapar(tokens)
    y.read('src/yapar/slr-2.yalp')
    print(y.grammar)
    print()
    print(y.tokens)
    print(list(y.yalex_tokens.keys()))
    print()
    print("FIRST(E) = ", y.first('E'))
    print("FIRST(T) = ", y.first('T'))
    print("FIRST(F) = ", y.first('F'))
    print()
    print(y.follow())
    print()
    y.build_lr0()
