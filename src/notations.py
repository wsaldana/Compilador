from utils.printer import print_return


class Notations:
    @classmethod
    @print_return("POSTFIX")
    def to_postfix(cls, infix):
        infix = list(infix)[::-1]
        opers = []
        postfix = []
        prec = {'*': 100, '.': 80, '|': 60, ')': 40, '(': 20}

        while infix:
            c = infix.pop()

            if c == '(':
                opers.append(c)

            elif c == ')':
                while opers[-1] != '(':
                    postfix.append(opers.pop())
                opers.pop()

            elif c in prec:
                while opers and prec[c] < prec[opers[-1]]:
                    postfix.append(opers.pop())
                opers.append(c)

            else:
                postfix.append(c)

        while opers:
            postfix.append(opers.pop())

        return ''.join(postfix)
