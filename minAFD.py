import AFD

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

