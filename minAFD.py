import AFD
import json
import time

class minAFD:
    def __init__(self, afd):
        self.afd = afd
        
    def createPartition(self, particion, transiciones):
        numParticion = len(particion)
        newParticion = particion.copy()
        aceptacion = newParticion.pop()
        newTransiciones = {}
        tempPart = {}
        
        for transicion in transiciones:
            if list(transicion) not in self.afd.afd_aceptacion:
                newTransiciones[transicion] = []
                for t in transiciones[transicion]:
                    for part in particion:
                        if transiciones[transicion][t] in part:
                            newTransiciones[transicion].append([transiciones[transicion][t],particion.index(part)])
        
        for transicion in newTransiciones:
            signs = []
            for elem in newTransiciones[transicion]:
             signs.append(elem[1])
             
            if tuple(signs) not in tempPart:
                tempPart[tuple(signs)] = []
            tempPart[tuple(signs)].append(transicion)
        
        newParticion = []
        for key in tempPart:
            newParticion.append(list(list(elem) for elem in tempPart[key]))
        
        newParticion.append(aceptacion)
        
        return newParticion
        

    def rmUnreachableStates(self, transiciones, inicio):
        estados = [inicio]

        for estado in estados:
            for transicion in transiciones[tuple(estado)]:
                if transiciones[tuple(estado)][transicion] not in estados:
                    estados.append(transiciones[tuple(estado)][transicion])
                    
        return estados
    
    def parseTransiciones(self):
        afd_transiciones = self.afd.afd_transiciones
        minTransiciones = {}
        for transicion in afd_transiciones:
            if tuple(transicion[0]) not in minTransiciones:
                minTransiciones[tuple(transicion[0])] = {}
            minTransiciones[tuple(transicion[0])][transicion[1]] = transicion[2]
            
        return minTransiciones
    
    def unParseTransiciones(self, transiciones):
        minTransiciones = []
        for transicion in transiciones:
            for key in transiciones[transicion]:
                minTransiciones.append([list(transicion), key, transiciones[transicion][key]])
                
        return minTransiciones
     

    def minimize(self):
        self.transiciones = self.parseTransiciones()
        self.estados = self.rmUnreachableStates( self.transiciones, self.afd.afd_inicial)
        self.partition = [[],[]]
        for estado in self.estados:
            if estado not in self.afd.afd_aceptacion:
                self.partition[0].append(estado)
            elif estado in self.afd.afd_aceptacion:
                self.partition[1].append(estado)
        
        self.partition = self.createPartition(self.partition, self.transiciones)

        while True:
            nParticion = self.createPartition(self.partition, self.transiciones)
            if self.partition != nParticion:
                self.partition = nParticion   
            else:
                break
            
        self.estados = [j for j in self.partition]
        
        tempTrans = {}
        
        for estado in self.estados:
            tEstado = tuple(tuple(elem) for elem in estado)
            for key in self.transiciones[tuple(estado[0])]:
                for part in self.partition:
                    if self.transiciones[tuple(estado[0])][key] in part:
                        if tEstado not in tempTrans:
                            tempTrans[tEstado] = {}
                        tempTrans[tEstado][key] = part
         
        self.transiciones = self.unParseTransiciones(tempTrans)
                        
                

    def get_minimized_afd(self):
        return {
            "ESTADOS": self.estados,
            "SIMBOLOS": self.afd.simbolos,
            "INICIO": self.find_start_state(),
            "ACEPTACION": self.estados[-1],
            "TRANSICIONES": self.transiciones
        }
        
    def find_start_state(self):
        for estado in self.estados:
            for i in estado:
                if i == self.afd.afd_inicial:
                    return estado
                
    def generar_json_minafd(self, nombre_archivo):
         
        afd_data = {
            "ESTADOS": self.estados,
            "SIMBOLOS": self.afd.simbolos,
            "INICIO": self.find_start_state(),
            "ACEPTACION": self.estados[-1],
            "TRANSICIONES": self.transiciones
        } 

        with open(nombre_archivo, 'w') as archivo:
            json.dump(afd_data, archivo, indent=4)
            
        print("Archivo JSON para minAFD generado con éxito.")

def get_path(actual, string, getString, transitions, track = [], count = 0, symbol = None):

    if string and getString:
        symbol = string[0]
        string = string[1:]
        getString = False
        
    for transition in transitions:
        if transition not in track:
            initial, transition_s, destination = transition
            if initial == actual and transition_s == symbol:
                count += 1
                track.append(transition)

                if transition_s == symbol:
                    getString = True
                if string == "":
                    symbol = ""
                    getString = False
                count = get_path(destination, string, getString, transitions, track, count, symbol)
    return count

def accepts_stack_minafd(string, actual, acceptation, transitions):
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
        if dest == acceptation and symbol == lastchar:
            return True, track
    return False, track
