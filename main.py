from Shunting_Yard import shunting_yard
from AFN import postfix_to_nfa, generate_nfa_json, accepts_stack
from AFD import AFD, accepts_stack_afd, createDFA
from minAFD import accepts_stack_minafd
from NFAtoDFA import NFAtoDFA
from minAFD import minAFD
import json


def main():
    expression = "(a+c)*b*aaa(b+c)"
    #expression = input("Ingrese la expresión regular")
    chain = ""

    try:
        postfix_expression = shunting_yard(expression)
        print("Expresión regular ingresada:", expression)
        print("Expresión en postfix:", postfix_expression)
        nfa = postfix_to_nfa(postfix_expression)
        # Crea el json del nfa para tener la descripcion del afn
        generate_nfa_json(nfa)

        dfa = createDFA("AFN.json")

        minDFA = minAFD(dfa)
        minDFA.minimize()
        minDFA.generar_json_minafd("minAFD.json")

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
                if transition[2] == acceptation:
                    break
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

        
        #dfa.generar_json_afd("AFD.json")
        #minDFA = minAFD(dfa)
        #minDFA.minimize()
        #print(minDFA.get_minimized_afd()

        print("\n---------------------------------- MIN AFD ----------------------------------\n")

        with open("minAFD.json", "r", encoding="utf-8") as json_file:
            minafd = json.load(json_file)

        initial = minafd["INICIO"]
        acceptation = minafd["ACEPTACION"]
        transitions = minafd["TRANSICIONES"]

        result, track = accepts_stack_minafd(string, initial, acceptation, transitions)

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

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()