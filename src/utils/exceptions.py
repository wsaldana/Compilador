class BadInfix(Exception):
    def __init__(
            self,
            message="Infix is wrong formatted"):
        self.message = message
        super().__init__(self.message)


class InfixNotBalanced(Exception):
    def __init__(
            self,
            message="Infix is not balanced"):
        self.message = message
        super().__init__(self.message)


class YalexSyntaxError(Exception):
    def __init__(self, message="Invalid syntax in yalex", line=None):
        if line:
            self.message = f"Invalid syntax in line {line} at yalex"
        else:
            self.message = message
        super().__init__(self.message)


class YalexUnexpectedSymbol(Exception):
    def __init__(self, message="Unexpected symbol in yalex", line=None):
        if line:
            self.message = f"Unexpected symbol in line {line} at yalex"
        else:
            self.message = message
        super().__init__(self.message)
