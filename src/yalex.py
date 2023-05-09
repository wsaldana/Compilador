from notations import build_tree, Notations, Node
from utils.exceptions import YalexSyntaxError, YalexUnexpectedSymbol


class Yalex:
    def __init__(self):
        self.dummies = []
        self.infix = ''
        self.dummy_placeholder_symbol = 'ю'
        self.reg_tokens = {}

    def regex_range(self, string):
        alf = '|'.join([chr(i) for i in range(65, 123) if i not in range(91, 97)])
        digs = '|'.join([str(i) for i in range(0, 10)])
        expanded = string.replace("['A'-'Z''a'-'z']", f'({alf})')
        expanded = expanded.replace("['0'-'9']", f'({digs})')
        expanded = expanded.replace("['+''-']", "('+'|'-')")
        expanded = expanded.replace('[\\s\\t\\n]', '(\\s|\\t|\\n)')
        return expanded

    def expand(self, regex):
        backlash_ops = {'n': '\n', 's': ' ', 't': '\t'}

        if regex[0] != '[':
            return regex.replace("['+''-']", "('+'|'-')")

        string = regex[2:-2]
        if regex[1] == "'":
            groups = string.split("''")
            res = ''
            for group in groups:
                if "-" in group:
                    group = '|'.join([
                        chr(i)
                        for i in range(ord(group[0]), ord(group[-1]) + 1)
                    ])
                res += f"|{group}"
            return f"({res[1:]})"

        if regex[1] == '"':
            chars = list(string)
            stack = []
            i = 0
            while len(chars) > 0:
                char = chars.pop(0)
                if char == '\\':
                    stack.append(backlash_ops[chars.pop(0)])
                else:
                    stack.append(char)
                i += 1

            return f"({'|'.join(stack)})"

    def read_yalex(self, file, dummy_placeholder=False):
        rule = False
        vars = {}
        infix = ''
        n_line = 2
        with open(file) as yal:
            for line in yal:
                if len(line) > 1:
                    try:
                        tokens = line.split()
                        if ("(*" in line and "*)" not in line) or ("*)" in line and "(*" not in line):
                            raise YalexSyntaxError(line=n_line)
                        if not tokens[0] == "(*":
                            if tokens[0] == 'let':
                                value = tokens[3]
                                sorted_keys = sorted(vars.keys(), key=len, reverse=True)
                                for var in sorted_keys:
                                    value = value.replace(var, vars[var])
                                    value = value.replace('\\+', '\\s')
                                value = self.expand(value)
                                vars[tokens[1]] = value
                            elif tokens[0] == 'rule':
                                if tokens[1] != 'tokens':
                                    print("ERROR: ", line)
                                    raise YalexSyntaxError(line=n_line)
                                rule = True
                                continue
                            elif rule:
                                pos = not tokens[0] == '|'
                                token = tokens[0] if pos else tokens[1]
                                dummy = tokens[3] if pos else tokens[4]
                                self.dummies.append(dummy)
                                if dummy_placeholder:
                                    dummy = self.dummy_placeholder_symbol
                                if token in vars.keys():
                                    dummy_token = f'|(({vars[token]}){dummy})'
                                    self.reg_tokens[dummy] = vars[token]
                                else:
                                    dummy_token = f'|(({token}){dummy})'
                                    self.reg_tokens[dummy] = token
                                infix += dummy_token
                            else:
                                print("ERROR: ", line)
                                raise YalexUnexpectedSymbol(line=n_line)
                    except:
                        print("ERROR: ", line)
                        raise YalexSyntaxError(line=n_line)
                n_line += 1
        self.infix = infix[1:]
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

    def write_lexical_analyzer(self, output_file_name):
        with open('src/output/lexical_analyzer.txt', 'r') as template:
            with open(output_file_name, 'w') as new_file:
                for line in template:
                    if line.startswith("postfixs ="):
                        new_line = "postfixs = " + str(self.reg_tokens_to_postfix()) + "\n"
                        new_file.write(new_line)
                    elif line.startswith("alphabets ="):
                        new_line = "alphabets = " + str(self.reg_tokens_alphabet()) + "\n"
                        new_file.write(new_line)
                    else:
                        new_file.write(line)

    def reg_tokens_to_postfix(self):
        return {
            k: Notations(v).to_postfix()
            for k, v in self.reg_tokens.items()
        }

    def reg_tokens_alphabet(self):
        return {
            k: Notations(v).get_alphabet(v)
            for k, v in self.reg_tokens.items()
        }


if __name__ == "__main__":
    y = Yalex()
    y.read_yalex('src/yalex/slr-2.yal')
    print(y.reg_tokens)
    print()

    print(y.reg_tokens_to_postfix())
    print()
    print(y.reg_tokens_alphabet())

    print()

    y.write_lexical_analyzer("src/output/prueba1.py")



    '''
    print(y.dummies)
    print("Infix:\n", ''.join(y.process_dummies(y.infix)))

    postfix = Notations(y.infix).to_postfix()
    print()
    print("Posfix:\n", ''.join(y.process_dummies(postfix)))

    root = build_tree(y.process_dummies(postfix))
    root.make_graph()
    '''
