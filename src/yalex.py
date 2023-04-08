from notations import build_tree, Node, Notations


class Yalex:
    def __init__(self):
        self.dummies = []
        self.infix = ''
        self.dummy_placeholder_symbol = 'ю'

    def regex_range(self, string):
        alf = '|'.join([chr(i) for i in range(65, 123) if i not in range(91, 97)])
        digs = '|'.join([str(i) for i in range(0, 10)])
        expanded = string.replace("['A'-'Z''a'-'z']", f'({alf})')
        expanded = expanded.replace("['0'-'9']", f'({digs})')
        expanded = expanded.replace("['+''-']", "('+'|'-')")
        expanded = expanded.replace('[\\s\\t\\n]', '(\\s|\\t|\\n)')
        return expanded

    def read_yalex(self, file, dummy_placeholder=False):
        rule = False
        vars = {}
        infix = ''
        with open(file) as yal:
            for line in yal:
                if len(line) > 1:
                    # line = line.replace("'", "").replace('"', '')
                    tokens = line.split()
                    if not tokens[0] == "(*":
                        if tokens[0] == 'let':
                            value = tokens[3].replace('"', '')
                            for var in vars.keys():
                                value = value.replace(var, vars[var])
                                value = value.replace('s', '+')
                                value = value.replace('\\+', '\\s')
                            vars[tokens[1]] = value
                        if tokens[0] == 'rule':
                            rule = True
                            continue
                        if rule:
                            pos = not tokens[0] == '|'
                            token = tokens[0] if pos else tokens[1]
                            dummy = tokens[3] if pos else tokens[4]
                            self.dummies.append(dummy)
                            if dummy_placeholder:
                                dummy = self.dummy_placeholder_symbol
                            if token in vars.keys():
                                dummy_token = f'|(({vars[token]}){dummy})'
                            else:
                                dummy_token = f'|(({token}){dummy})'
                            infix += dummy_token
        self.infix = self.regex_range(infix[1:])
        return self.infix

    def process_dummies(self, exp):
        infix = list(exp)
        while '\\' in infix:
            i = infix.index('\\')
            infix[i:i+2] = [''.join(infix[i:i+2])]

        while "'" in infix:
            i = infix.index("'")
            infix[i:i+3] = [''.join(infix[i:i+3])]

        dummies = self.dummies.copy()
        while self.dummy_placeholder_symbol in infix:
            infix = [
                dummies.pop(0)
                if i == self.dummy_placeholder_symbol
                else i
                for i in infix
            ]

        return infix


if __name__ == "__main__":
    y = Yalex()
    y.read_yalex('src/yalex/slr-2.yal', True)
    print("Infix:\n", ''.join(y.process_dummies(y.infix)))

    postfix = Notations(y.infix).to_postfix()
    print()
    print("Posfix:\n", ''.join(y.process_dummies(postfix)))

    root = build_tree(y.process_dummies(postfix))
    root.make_graph()
