from Shunting_Yard import shunting_yard
from AFN import postfix_to_nfa, generate_nfa_json, accepts_stack
from AFD import AFD, accepts_stack_afd
from NFAtoDFA import NFAtoDFA
from minAFD import minAFD
import json


def main():
    expression = "(a+c*)c*b"
    #expression = input("Ingrese la expresión regular")
    chain = ""

    try:
        postfix_expression = shunting_yard(expression)
        print("Expresión regular ingresada:", expression)
        print("Expresión en postfix:", postfix_expression)
        nfa = postfix_to_nfa(postfix_expression)
        # Crea el json del nfa para tener la descripcion del afn
        generate_nfa_json(nfa)

        string = input("Ingrese la cadena a evaluar: ")
        print("\n---------------------------------- AFN ----------------------------------\n")
        with open("AFN.json", "r", encoding="utf-8") as json_file:
            afn = json.load(json_file)
        initial = afn["INICIO"][0]
        acceptation = afn["ACEPTACION"][0]
        transitions = afn["TRANSICIONES"]
        result, track = accepts_stack(string, initial, acceptation, transitions)
        if result:
            print("SI")
            print("Transiciones realizadas:")
            for transition in track:
                print(f"Estado {transition[0]} --({transition[1]})--> Estado {transition[2]}")
        else:
            print("No")
            print("Transiciones realizadas:")
            for transition in track:
                print(f"Estado {transition[0]} --({transition[1]})--> Estado {transition[2]}")
        print("\n---------------------------------- AFD ----------------------------------\n")

        with open("AFD.json", "r", encoding="utf-8") as json_file:
            afd = json.load(json_file)

        initial = afd["INICIO"][0]
        acceptation = afd["ACEPTACION"][0]
        transitions = afd["TRANSICIONES"]

        result, track = accepts_stack_afd(string, initial, acceptation, transitions)

        if result:
            print("SI")
            print("Transiciones realizadas:")
            for transition in track:
                print(f"Estado {transition[0]} --({transition[1]})--> Estado {transition[2]}")
        else:
            print("No")
            print("Transiciones realizadas:")
            for transition in track:
                print(f"Estado {transition[0]} --({transition[1]})--> Estado {transition[2]}")


        #postfix_to_dfa(postfix_expression=postfix_expression)

        #dfa = NFAtoDFA().construir_afd("AFN.json")
        #dfa.generar_json_afd("AFD.json")
        #minDFA = minAFD(dfa)
        #minDFA.minimize()
        #print(minDFA.get_minimized_afd()

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()