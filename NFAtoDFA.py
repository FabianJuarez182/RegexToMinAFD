from AFN import *
from AFD import *
import json

class NFAtoDFA:
    def __init__(self):
        
            
        self.afd_transiciones = []
        self.afd_estados = []
        self.afd_aceptacion = []
        
    def construir_afd(self, filename):
        # Leer el archivo JSON que contiene la descripción del AFN.
        with open(filename, "r", encoding="utf-8") as json_file:
            afn = json.load(json_file)
        
        self.estados = afn["ESTADOS"]
        self.simbolos = afn["SIMBOLOS"]
        self.inicio = afn["INICIO"]
        self.aceptacion = afn["ACEPTACION"]
        self.transiciones = afn["TRANSICIONES"]
        
        self.afd_estados.append(self.inicio)
        
        for estado in self.afd_estados:
            tempState = {}
            for simbolo in self.simbolos:
                if simbolo != "ε":
                    tempState[simbolo] = []
                    
            for trans in self.transiciones:
                for elemento in estado:
                    if trans[0] is elemento:               
                        if trans[1] == "ε":
                            for key in tempState:
                                if trans[2] not in tempState[key]:
                                    tempState[key].append(trans[2])
                        else:
                            if trans[2] not in tempState[trans[1]]:
                                tempState[trans[1]].append(trans[2])
                            
            if tempState:
                for key in tempState:
                    tempState[key].sort()
                    if tempState[key]: 
                        if tempState[key] not in self.afd_estados:
                            self.afd_estados.append(tempState[key])
                        self.afd_transiciones.append([
                            estado,
                            key,
                            tempState[key]
                        ])
            for elemento in estado:
                if self.aceptacion[0] == elemento:
                    self.afd_aceptacion.append(estado)
                    break
        self.simbolos.remove("ε")
        
        return AFD(self.afd_transiciones, self.simbolos, self.afd_estados, self.afd_estados[0],self.afd_aceptacion)

