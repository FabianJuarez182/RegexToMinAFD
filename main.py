from Shunting_Yard import shunting_yard
from AFN import postfix_to_nfa, generate_nfa_json, accepts_stack
from AFD import AFD, postfix_to_dfa
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



        string = input("Ingrese la cadena a evaluar")
        with open("AFN.json", "r", encoding="utf-8") as json_file:
            afn = json.load(json_file)
        initial = afn["INICIO"][0]
        acceptation = afn["ACEPTACION"][0]
        transitions = afn["TRANSICIONES"]
        res = "SI" if accepts_stack(string, initial, acceptation, transitions) else "NO"
        print(res)


        # Crea el json del nfa para tener la descripcion del afn
        generate_nfa_json(nfa)
        
        postfix_to_dfa(postfix_expression=postfix_expression)

        #dfa = NFAtoDFA().construir_afd("AFN.json")
        #dfa.generar_json_afd("AFD.json")
        #minDFA = minAFD(dfa)
        #minDFA.minimize()
        #print(minDFA.get_minimized_afd()

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()