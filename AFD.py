from AFN import *
import json

class AFD:
    def __init__(self, transiciones, simbolos, estados, aceptacion):
        self.afd_transiciones = transiciones
        self.simbolos = simbolos
        self.afd_estados = estados
        self.afd_aceptacion = aceptacion

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
        
def postfix_to_dfa(postfix_expression):
    print(postfix_expression)
