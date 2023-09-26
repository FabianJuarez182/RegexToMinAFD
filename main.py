from Shunting_Yard import shunting_yard
from AFN import postfix_to_nfa, generate_nfa_json
from AFD import AFD, createDFA
from NFAtoDFA import NFAtoDFA
from minAFD import minAFD


def main():
    expression = "(a+c*)c*^b"
    chain = ""

    try:
        postfix_expression = shunting_yard(expression)
        print("Expresión regular ingresada:", expression)
        print("Expresión en postfix:", postfix_expression)
        nfa = postfix_to_nfa(postfix_expression)

        # Crea el json del nfa para tener la descripcion del afn
        generate_nfa_json(nfa)
        
        afd = createDFA("AFN.json")

        #dfa = NFAtoDFA().construir_afd("AFN.json")
        #dfa.generar_json_afd("AFD.json")
        #minDFA = minAFD(dfa)
        #minDFA.minimize()
        #print(minDFA.get_minimized_afd())

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()