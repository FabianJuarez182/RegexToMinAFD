import AFD

class minAFD:
    def __init__(self, afd):
        self.afd = afd
        self.partition = []
        
    def createPartition(self, estados, aceptacion):
        for elem in aceptacion:
            estados.remove(elem)
            
        self.partition = [[set(estado) for estado in estados], [set(estado) for estado in estados]]

    def minimize(self):
        self.createPartition(self.afd.afd_estados, self.afd.afd_aceptacion)
        refined = True
        while refined:
            refined = False
            for symbol in self.afd.simbolos:
                new_partition = []
                for block in self.partition:
                    transitions = {}
                    for state in block:
                        for transition in self.afd.afd_transiciones:
                            if state == transition[0] and symbol == transition[1]:
                                print(transitions)
                                if transition[2] not in transitions:
                                    transitions[transition[2]] = [state]
                                else:
                                    transitions[transition[2]].append(state)
                    for key in transitions:
                        new_partition.append(set(transitions[key]))
                if len(new_partition) > 0 and len(new_partition) != len(self.partition):
                    refined = True
                    self.partition = new_partition
        self.generate_minimized_afd()

    def generate_minimized_afd(self):
        self.afd_minimized_states = []
        self.afd_minimized_transitions = []
        self.afd_minimized_acceptance = []

        for block in self.partition:
            self.afd_minimized_states.append(list(block))
            for state in block:
                if state in self.afd.afd_aceptacion:
                    self.afd_minimized_acceptance.append(list(block))

        for i, state_set in enumerate(self.partition):
            for symbol in self.afd.simbolos:
                next_state = self.find_next_state(state_set, symbol)
                self.afd_minimized_transitions.append([list(state_set), symbol, next_state])

    def find_next_state(self, state_set, symbol):
        for transition in self.afd.afd_transiciones:
            if transition[0] in state_set and transition[1] == symbol:
                for block in self.partition:
                    if transition[2] in block:
                        return list(block)
        return []

    def get_minimized_afd(self):
        return {
            "ESTADOS": self.afd_minimized_states,
            "SIMBOLOS": self.afd.simbolos,
            "INICIO": self.find_start_state(),
            "ACEPTACION": self.afd_minimized_acceptance,
            "TRANSICIONES": self.afd_minimized_transitions
        }

    def find_start_state(self):
        for block in self.partition: 
            if {self.afd.afd_estados[0][0]} in block:
                return {self.afd.afd_estados[0][0]}