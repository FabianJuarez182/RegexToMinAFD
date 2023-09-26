from AFN import *
import json

class AFD:
    def __init__(self, filename):
        # Leer el archivo JSON que contiene la descripción del AFN.
        with open(filename, "r") as json_file:
            afn = json.load(json_file)
            
        
        self.afd_transiciones = []
        self.afd_estados = []
        self.afd_aceptacion = []
        self.construir_afd(afn)
        
        self.generar_json_afd("AFD.json")
        

   

    def construir_afd(self, afn):
        self.estados = afn["ESTADOS"]
        self.simbolos = afn["SIMBOLOS"]
        self.inicio = afn["INICIO"]
        self.aceptacion = afn["ACEPTACION"]
        self.transiciones = afn["TRANSICIONES"]
        
        self.afd_estados.append(self.inicio)
        
        for estado in self.afd_estados:
            tempState = {}
            for simbolo in self.simbolos:
                if simbolo != "\u03b5":
                    tempState[simbolo] = []
                    
            for trans in self.transiciones:
                for elemento in estado:
                    if trans[0] is elemento:               
                        if trans[1] == "\u03b5":
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
        self.simbolos.remove("\u03b5")
                         
                
                
                
                
                

    def generar_json_afd(self, nombre_archivo):
        afd_data = {
            "ESTADOS": [list(map(int, estado)) for estado in self.afd_estados],
            "SIMBOLOS": self.simbolos,
            "INICIO": [list(map(int, self.afd_estados[0]))],
            "ACEPTACION": [list(map(int, estado)) for estado in self.afd_aceptacion],
            "TRANSICIONES": [ [list(map(int, origen)), simbolo, list(map(int, destino))]
                for origen, simbolo, destino in self.afd_transiciones
                ]
        }

        with open(nombre_archivo, 'w') as archivo:
            json.dump(afd_data, archivo, indent=4)
            
        print("Archivo JSON para AFD generado con éxito.")
