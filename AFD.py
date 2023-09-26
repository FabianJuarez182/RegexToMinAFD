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
        
        afd.generar_json_afd("AFDp.py")
        

def subset_construction(nfa):
    dfa_states = []  
    dfa_start_state = epsilon_closure(nfa, nfa.start_state)
    
    dfa_states.append(dfa_start_state)  


def epsilon_closure(nfa, state):
    

    return closure


        
def parseDFA(states, alphabet, transitions, start_state, accept_states):
    states = [list(elem) for elem in states if elem]
    alphabet.remove('ε')

    return AFD(states, alphabet, transitions, start_state, accept_states)

