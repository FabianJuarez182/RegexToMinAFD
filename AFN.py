import time
import json
def alphanum(a):
    return a.isalpha() or a.isnumeric() or a == "ε"

class state:
    label, ledge, redge = None, None, None
    state_count = 0 # Contador de estados
    def __init__(self):
        self.state_num = state.state_count
        state.state_count += 1

class nfa:

    def __init__(self, initial, acceptation):
        self.initial, self.acceptation = initial, acceptation




def postfix_to_nfa(regex):

    stack = []

    for symbol in regex:
        if alphanum(symbol):
            # Crear un nuevo estado para el símbolo
            new_initial, new_accepting = state(), state()

            new_initial.label, new_initial.ledge = symbol, new_accepting

            

            stack.append(nfa(new_initial, new_accepting))
            
        elif symbol == '^':
            # Concatenación
            state2, state1 = stack.pop(), stack.pop()
            state1.acceptation = state2
            lastf, lasts = None, None
            l1 = state1.initial.label

            if l1 is None:
                l1 = state1.initial.ledge

                while l1 is not None:
                    l1 = l1.ledge
                    if l1:
                        lastf = l1                
                l1 = lastf.label

            if lastf:
                lastf.ledge = state2.initial.ledge
                lastf.redge = state2.initial.redge
                if lastf.ledge:
                    lastf.ledge.label = state2.initial.label
                if lastf.redge:
                    lastf.redge.label = state2.initial.label
                
            else:
                state1.ledge = state2.initial.ledge
                state1.redge = state2.initial.redge
                if state1.ledge:
                    state1.ledge.label = state2.initial.label
                if state1.redge:
                    state1.redge.label = state2.initial.label

            stack.append(nfa(state1.initial, state2.acceptation))
        elif symbol == '+':
            # Unión
            second = stack.pop()
            first = stack.pop()
            new_initial, new_accepting = state(), state()
            lastf, lasts = None, None
            new_accepting.label = "ε"

            l1 = first.initial.label

            if l1 is None:
                l1 = first.initial.ledge

                while l1 is not None:
                    l1 = l1.ledge
                    if l1:
                        lastf = l1
                
                l1 = lastf.label

            l2 = second.initial.label

            if l2 is None:
                l2 = second.initial.ledge

                while l2 is not None:
                    l2 = l2.ledge
                    if l2:
                        lasts = l2
                
                l2 = lasts.label

            first.initial.label, second.initial.label = "ε", "ε"
            new_initial.ledge, new_initial.redge = first.initial, second.initial


            new_first, new_second = state(), state()
            new_first.label, new_second.label = l1, l2


            if lastf and lasts:
                lastf.ledge, lasts.ledge = new_first, new_second
            elif lastf:
                lastf.ledge, second.initial.ledge = new_first, new_second
            elif lasts:
                first.initial.ledge , lasts.ledge = new_first, new_second
            else:
                first.initial.ledge, second.initial.ledge = new_first, new_second

            new_first.ledge, new_second.ledge = new_accepting, new_accepting


            stack.append(nfa(new_initial, new_accepting))

        elif symbol == '*':
            state1 = stack.pop()
            new_initial, new_accepting, new_transition = state(), state(), state()

            new_accepting.label = "ε"
            new_transition.label = "ε"

            new_initial.ledge, new_initial.redge = new_transition, new_accepting

            new_transition.ledge = state1.initial

            state1.initial.ledge, state1.initial.redge = new_accepting, new_transition

            state1.acceptation.ledge, state1.acceptation.redge = state1.initial, new_accepting

            stack.append(nfa(new_initial, new_accepting))

    if len(stack) != 1:
        raise ValueError("Expresión no válida")

    return stack.pop()


def obtener_estados(nfa):
    estados = set()
    stack = [nfa.initial]
    
    while stack:
        estado = stack.pop()
        if estado.state_num not in estados:  # Verifica si el estado ya se ha agregado
            estados.add(estado.state_num)
            if estado.ledge:
                stack.append(estado.ledge)
            if estado.redge:
                stack.append(estado.redge)

    return list(estados)

def generate_nfa_json(nfa):

    todos_estados =  obtener_estados(nfa)

    symbols_set = set()

    nfa_json = {
        "ESTADOS": todos_estados,
        "SIMBOLOS": [],
        "INICIO": [nfa.initial.state_num],
        "ACEPTACION": [nfa.acceptation.state_num],
        "TRANSICIONES": []
    }

    transitions = {}
    processed_states = set()
    stack = [nfa.initial]

    while stack:
        current_state = stack.pop()

        # Verificar si el estado ya ha sido procesado
        if current_state in processed_states:
            continue

        # Marcar el estado como procesado
        processed_states.add(current_state)

        if current_state not in transitions:
            transitions[current_state] = []

        if current_state.ledge:
            transitions[current_state].append((current_state.ledge.label, current_state.ledge))
            stack.append(current_state.ledge)
            # Agregar el símbolo al conjunto
            if current_state.ledge.label is not None:
                symbols_set.add(current_state.ledge.label)

        if current_state.redge:
            transitions[current_state].append((current_state.redge.label, current_state.redge))
            stack.append(current_state.redge)
            # Agregar el símbolo al conjunto
            if current_state.redge.label is not None:
                symbols_set.add(current_state.redge.label)

    # Convertir el conjunto de símbolos en una lista ordenada
    nfa_json["SIMBOLOS"] = sorted(list(symbols_set))

    for state, state_transitions in transitions.items():
        for symbol, target_state in state_transitions:
            if target_state.label is None:
                target_state.label = "ε"
            nfa_json["TRANSICIONES"].append((state.state_num, target_state.label, target_state.state_num))

    with open("AFN.json", "w", encoding="utf-8") as json_file:
        json.dump(nfa_json, json_file, indent=4, ensure_ascii=False)
    print("Archivo JSON para AFN generado con éxito.")


def get_path(actual, string, getString, transitions, track = [], count = 0, symbol = None):

    if string and getString:
        symbol = string[0]
        string = string[1:]
        getString = False
        
    for transition in transitions:
        if transition not in track or count <= 600:
            initial, transition_s, destination = transition
            if initial == actual and (transition_s == symbol or transition_s == "ε" or transition_s is None):
                count += 1
                track.append(transition)

                if transition_s == symbol:
                    getString = True
                
                count = get_path(destination, string, getString, transitions, track, count, symbol)
    return count

def accepts_stack(string, actual, acceptation, transitions):
    if not string:
        return actual in acceptation, []

    track = []
    lastchar = string[-1]

    start = time.time() * 1000
    time.sleep(1)
    counter = get_path(actual, string, True, transitions, track)
    end = time.time() * 1000
    time.sleep(1)
    running = end - start
    print(f"Se requirieron {running} milisegundos para verificar la cadena.")
    
    for transition in track:
        ini, symbol, dest = transition
        if dest == acceptation and symbol == lastchar or symbol == "ε" or symbol is None:
            return True, track
    return False, track
    




            

