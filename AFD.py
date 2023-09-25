from AFN import * 
from collections import deque

class AFD:
    def __init__(self, nfa):
       self.initialState, self.acceptingState, self.transtions = nfa_to_dfa(nfa)
       
class dfa_state:
    def __init__(self, nfa_states):
        self.nfa_states = nfa_states
        self.transitions = {}
        
def nfa_to_dfa(nfa):
    # Initialize the DFA with the epsilon closure of the NFA's initial state
    initial_nfa_states = epsilon_closure(nfa.initial)
    dfa_initial_state = dfa_state(initial_nfa_states)

    dfa_states = [dfa_initial_state]
    unprocessed_dfa_states = deque([dfa_initial_state])
    dfa_transitions = {}

    while unprocessed_dfa_states:
        current_dfa_state = unprocessed_dfa_states.popleft()
        for symbol in get_input_symbols(nfa):
            # Get the epsilon closure of the NFA states reachable from the current state with the symbol
            reachable_nfa_states = set()
            for nfa_state in current_dfa_state.nfa_states:
                if symbol in nfa_state.transitions:
                    reachable_nfa_states.update(nfa_state.transitions[symbol])

            epsilon_reachable_nfa_states = set()
            for nfa_state in reachable_nfa_states:
                epsilon_reachable_nfa_states.update(epsilon_closure(nfa_state))

            if epsilon_reachable_nfa_states:
                # Create a new DFA state or reuse an existing one
                next_dfa_state = None
                for state in dfa_states:
                    if state.nfa_states == epsilon_reachable_nfa_states:
                        next_dfa_state = state
                        break

                if next_dfa_state is None:
                    next_dfa_state = dfa_state(epsilon_reachable_nfa_states)
                    dfa_states.append(next_dfa_state)
                    unprocessed_dfa_states.append(next_dfa_state)

                current_dfa_state.transitions[symbol] = next_dfa_state
                dfa_transitions[(current_dfa_state, symbol)] = next_dfa_state

    # Identify the accepting states of the DFA based on the NFA's accepting states
    dfa_accepting_states = [state for state in dfa_states if any(nfa_state.acceptation for nfa_state in state.nfa_states)]

    return dfa_initial_state, dfa_accepting_states, dfa_transitions

def epsilon_closure(nfa_state):
    # Compute the epsilon closure of an NFA state using depth-first search
    epsilon_closure_set = set()
    stack = [nfa_state]

    while stack:
        current_state = stack.pop()
        epsilon_closure_set.add(current_state)
        for epsilon_transition in current_state.epsilon_transitions:
            if epsilon_transition not in epsilon_closure_set:
                stack.append(epsilon_transition)

    return epsilon_closure_set

def get_input_symbols(nfa):
    # Get the input symbols from the NFA's transitions
    input_symbols = set()
    stack = [nfa.initial]

    while stack:
        current_state = stack.pop()
        for symbol in current_state.transitions.keys():
            input_symbols.add(symbol)
        for next_state in current_state.transitions.values():
            stack.extend(next_state)

    return input_symbols
       
       
