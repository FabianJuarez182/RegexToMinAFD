from AFN import *
import json

class AFD:
    def __init__(self, estados, simbolos, transiciones, inicial, aceptacion):
        
        self.afd_transiciones = transiciones
        
        self.simbolos = simbolos
        self.afd_estados = estados
        self.afd_inicial = inicial
        self.afd_aceptacion = aceptacion


    def generar_json_afd(self, nombre_archivo):
        
        afd_data = {
            "ESTADOS": [list(map(int, estado)) for estado in self.afd_estados],
            "SIMBOLOS": self.simbolos,
            "INICIO": [list(map(int, self.afd_inicial))],
            "ACEPTACION": [list(map(int, estado)) for estado in self.afd_aceptacion],
            "TRANSICIONES": [ [list(map(int, origen)), simbolo, list(map(int, destino))]
                for origen, simbolo, destino in self.afd_transiciones
                ]
        }

        with open(nombre_archivo, 'w') as archivo:
            json.dump(afd_data, archivo, indent=4)
            
        print("Archivo JSON para AFD generado con éxito.")
       
class nfaTemp:
    def __init__(self, estados, simbolos, inicial, aceptacion, transiciones):
        self.states = estados
        self.alphabet = simbolos
        self.start_state = inicial[0]
        self.accept_states = aceptacion
        self.transitions = {} 
        for transicion in transiciones:
            if transicion[0] not in self.transitions:
                self.transitions[transicion[0]] = {}
            if transicion[1] not in self.transitions[transicion[0]]:
                self.transitions[transicion[0]][transicion[1]] = []   
            self.transitions[transicion[0]][transicion[1]].append(transicion[2])
                
        

      
def createDFA(filename):
    # Leer el archivo JSON que contiene la descripción del AFN.
        with open(filename, "r", encoding="utf-8") as json_file:
            afn = json.load(json_file)
        
        afn = nfaTemp(afn["ESTADOS"],afn["SIMBOLOS"],afn["INICIO"],afn["ACEPTACION"],afn["TRANSICIONES"])
        afd = subset_construction(afn)
        
        afd.generar_json_afd("AFD.json")
        
        return afd
        

def subset_construction(nfa):
    dfa_states = []  
    dfa_transitions = {}
    dfa_start_state = epsilon_closure(nfa, [nfa.start_state])
    dfa_aceptation = []
    
    dfa_states.append(dfa_start_state)  

    for state in dfa_states:
        print(state)
        tempTrans = {}
        for simbolo in nfa.alphabet:
            if simbolo != "ε":
                paso = []
                for num in state:
                    if num in nfa.transitions:
                        if simbolo in nfa.transitions[num]:
                            for i in nfa.transitions[num][simbolo]:
                                paso.append(i)
                    if num in nfa.accept_states and state not in dfa_aceptation:
                        dfa_aceptation.append(state)
                        
                if paso:
                    ne = epsilon_closure(nfa,paso)
                    ne.sort()
                    tempTrans[simbolo] = ne
                    if tempTrans[simbolo] not in dfa_states:
                        dfa_states.append(tempTrans[simbolo])
                

        dfa_transitions[tuple(state)] = tempTrans
        
        
            
        
    dfa_states, dfa_transitions = checkTState(nfa, dfa_states, dfa_transitions)
    
    nfa.alphabet.remove("ε")
    
    tempTransiciones = []
    for trans in dfa_transitions:
        for simbolo in dfa_transitions[trans]:
            tempTransiciones.append([trans, simbolo, dfa_transitions[trans][simbolo]])
    dfa_transitions = tempTransiciones
    
    
    return AFD(dfa_states, nfa.alphabet, dfa_transitions, dfa_start_state, dfa_aceptation)


def epsilon_closure(nfa, state):
    stack = []
    closure = state
    for key in nfa.transitions:
        if key in closure:
            for keys in nfa.transitions[key]:
                if keys == "ε":
                    for elem in nfa.transitions[key][keys]:
                        stack.append(elem)

    while stack:
        elems = stack.pop()
        if elems not in closure:
            closure.append(elems)
            for key in nfa.transitions:
                if key == elems:
                    for keys in nfa.transitions[key]:
                        if keys == "ε":
                            for elem in nfa.transitions[key][keys]:
                                stack.append(elem)
    
    return closure

def checkTState(nfa, states, transitions):
    absolvente = [max(nfa.states) + 1]
    for state in states:
        for simbolo in nfa.alphabet:
            if simbolo != "ε":
                if tuple(state) in transitions and simbolo not in transitions[tuple(state)]:
                    if absolvente not in states:
                        states.append(absolvente)
                        transitions[tuple(absolvente)] = {}
                    transitions[tuple(state)][simbolo] = absolvente
        transitions[tuple(state)] = dict(sorted(transitions[tuple(state)].items()))
                
    return states, transitions     


        
def parseDFA(states, alphabet, transitions, start_state, accept_states):
    states = [list(elem) for elem in states if elem]
    alphabet.remove('ε')

    return AFD(states, alphabet, transitions, start_state, accept_states)

