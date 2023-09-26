from AFN import *
import json

class AFD:
    def __init__(self, filename):
        # Leer el archivo JSON que contiene la descripción del AFN.
        with open(filename, "r") as json_file:
            afd = convert_afn_to_afd(json.load(json_file))

        # Escribir el AFD resultante en un nuevo archivo JSON.
        with open("afd.json", "w") as json_file:
            json.dump(afd, json_file, indent=4)

        print("Conversión de AFN a AFD completada. Se ha generado afd.json.")

def epsilon_closure(afn, states):
    closure = set(states)
    stack = list(states)

    while stack:
        current_state = stack.pop()
        if "ε" in afn["TRANSICIONES"]:
            for target_state in afn["TRANSICIONES"][current_state]["ε"]:
                if target_state not in closure:
                    closure.add(target_state)
                    stack.append(target_state)

    return closure

def move(afn, states, symbol):
    move_states = set()
    for state in states:
        if symbol in afn["TRANSICIONES"][state]:
            move_states.update(afn["TRANSICIONES"][state][symbol])
    return move_states

def convert_afn_to_afd(afn):
    afd = {
        "ESTADOS": [],
        "SIMBOLOS": afn["SIMBOLOS"],
        "INICIO": None,
        "ACEPTACION": [],
        "TRANSICIONES": {}
    }

    # Calcula el estado inicial del AFD mediante la epsilon-cerradura del estado inicial del AFN.
    initial_state = epsilon_closure(afn, [afn["INICIO"]])
    afd["INICIO"] = initial_state

    # Inicializa una lista de estados no procesados.
    unprocessed_states = [initial_state]

    # Procesa estados hasta que no queden por procesar.
    while unprocessed_states:
        current_states = unprocessed_states.pop()
        afd["ESTADOS"].append(current_states)

        for symbol in afn["SIMBOLOS"]:
            if symbol != "ε":
                move_states = move(afn, current_states, symbol)
                if move_states:
                    move_states = epsilon_closure(afn, move_states)
                    afd["TRANSICIONES"][current_states, symbol] = move_states
                    if move_states not in afd["ESTADOS"] and move_states not in unprocessed_states:
                        unprocessed_states.append(move_states)

    # Determina los estados de aceptación del AFD.
    for state in afd["ESTADOS"]:
        if afn["ACEPTACION"] in state:
            afd["ACEPTACION"].append(state)

    return afd
