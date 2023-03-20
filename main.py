from src.afn import Thompson
from src.afd import Subconjuntos, minimize_dfa
from src.notations import Notations


def run():
    regex = '(a|b)*(b|a)*abb'
    w = 'ababb'

    notation = Notations(regex)
    postfix = notation.to_postfix()
    alphabet = notation.get_alphabet(regex)
    print("Postfix: ", postfix, "\n")

    thompson = Thompson(postfix, alphabet)
    nfa = thompson.construct()
    thompson.graph(nfa)
    rs1 = thompson.simulate(w)
    print(f"AFN: {w} {rs1} es aceptada")
    print(nfa, "\n")

    sub = Subconjuntos(nfa, alphabet)
    dfa = sub.construct()
    sub.graph(dfa)
    rs = sub.simulate(w)
    print(f"AFD: {w} {rs} es aceptada")
    print(dfa)

    mini = minimize_dfa(dfa)
    print()
    print(mini)
    sub.graph(mini)


if __name__ == "__main__":
    run()
