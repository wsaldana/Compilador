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
