class MyState():
    def __init__(self, n_state):
        """Estado del automata

        Args:
            n_state (int): Número que representa el estado
        """
        self.n_state = n_state

    def __str__(self):
        return str(self.n_state)

    def __repr__(self):
        return str(self)


class Transition():
    def __init__(
            self,
            state_i,
            label,
            state_f
    ):
        """Transiciones del autómata

        Args:
            state_i (MyState): Estado inicial
            state_f (MyState): Estado final
            label (str): Símbolo que representa la transición
        """
        self.state_i = state_i
        self.state_f = state_f
        self.label = label

    def __str__(self):
        return f"({self.state_i}, {self.label}, {self.state_f})"

    def __repr__(self):
        return str(self)


class Automata():
    def __init__(
            self,
            state_i,
            state_f,
            n_states,
            transitions,
            states
    ):
        """Automata Finito Determinista

        Args:
            state_i (str): MyState inicial
            state_f (str): MyState de aceptación
            n_states (int): Número de estados
            transitions (Transition): Transiciones del autómata
            states (MyState): MyStates del autómata
        """
        self.n_states = n_states
        self.states = states
        self.state_i = state_i
        self.state_f = state_f
        self.transitions = transitions

    def __str__(self):
        string = (
            f"Estados: {self.states} \n"
            f"Inicial: {self.state_i} \n"
            f"Aceptación: {self.state_f} \n"
            f"Tabla de transiciones: {self.transitions}"
        )
        return string

    def __repr__(self) -> str:
        return str(self)
