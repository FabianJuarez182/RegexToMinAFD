from graphviz import Digraph

class NFAState:
    def __init__(self):
        self.transitions = {}
        self.epsilon_transitions = set()
        self.accepting = False

def postfix_to_nfa(expression):
    stack = []

    for symbol in expression:
        if symbol.isalpha():
            # Crear un nuevo estado para el símbolo
            state = NFAState()
            state.transitions[symbol] = set()
            stack.append(state)
        elif symbol == '^':
            # Concatenación
            second = stack.pop()
            first = stack.pop()
            for s in first.transitions:
                first.transitions[s] |= second.epsilon_transitions
            stack.append(first)
        elif symbol == '+':
            # Unión
            second = stack.pop()
            first = stack.pop()
            state = NFAState()
            state.epsilon_transitions.add(first)
            state.epsilon_transitions.add(second)
            stack.append(state)
        elif symbol == '*':
            # Cierre de Kleene
            state = stack.pop()
            new_state = NFAState()
            new_state.epsilon_transitions.add(state)
            state.epsilon_transitions.add(new_state)
            stack.append(new_state)

    if len(stack) != 1:
        raise ValueError("Expresión no válida")

    return stack[0]

def visualize_nfa(nfa):
    dot = Digraph(format='png')
    dot.attr(rankdir='LR')  # Orientación izquierda a derecha

    # Crear un diccionario para mapear estados a nombres
    state_names = {}
    state_counter = 0

    # Agregar estados y transiciones al gráfico DOT
    def add_state_to_dot(state):
        nonlocal state_counter
        state_name = f"q{state_counter}"
        state_names[state] = state_name
        state_counter += 1
        dot.node(state_name, shape='circle', style='bold' if state.accepting else '')

        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                next_state_name = state_names.get(next_state, f"q{state_counter}")
                dot.edge(state_name, next_state_name, label=symbol)

        for next_state in state.epsilon_transitions:
            next_state_name = state_names.get(next_state, f"q{state_counter}")
            dot.edge(state_name, next_state_name, label='ε')

    # Recorrer el NFA y agregar estados al gráfico DOT
    stack = [nfa]
    while stack:
        current_state = stack.pop()
        add_state_to_dot(current_state)
        for next_state in current_state.transitions.values():
            for state in next_state:
                if state not in state_names:
                    stack.append(state)

    # Guardar el gráfico DOT como una imagen PNG
    dot.render('nfa', view=True)

    print("Imagen del AFN generada con éxito como 'nfa.png'.")

