from src.afn import Thompson
from src.afd import Subconjuntos, minimize_dfa
from src.notations import Notations, build_tree


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
    sub.graph(mini, export_name='ADF_MIN')

    root = build_tree(postfix)
    root.make_graph()


if __name__ == "__main__":
    run()
