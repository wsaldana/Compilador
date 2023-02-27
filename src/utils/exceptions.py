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
