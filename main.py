from Shunting_Yard import shunting_yard
from AFN import postfix_to_nfa, generate_nfa_json
from AFD import AFD


def main():
    expression = "(a+c*)c*b"
    chain = ""

    try:
        postfix_expression = shunting_yard(expression)
        print("Expresión regular ingresada:", expression)
        print("Expresión en postfix:", postfix_expression)
        nfa = postfix_to_nfa(postfix_expression)

        # Crea el json del nfa para tener la descripcion del afn
        generate_nfa_json(nfa)

        dfa = AFD("AFN.json")

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()