from graphviz import Digraph
def alphanum(a):
    return a.isalpha() or a.isnumeric() or a == "ε"

class state:
    label, ledge, redge = None, None, None

class nfa:

    def __init__(self, initial, acceptation):
        self.initial, self.acceptation = initial, acceptation

def postfix_to_nfa(expression):
    stack = []

    for symbol in expression:
        if alphanum(symbol):
            # Crear un nuevo estado para el símbolo
            new_accepting, new_initial = state(), state()

            new_initial.label, new_initial.ledge = symbol, new_accepting

            stack.append(nfa(new_initial, new_accepting))
            
        elif symbol == '^':
            # Concatenación
            state2, state1 = stack.pop(), stack.pop()
            state1.acceptation.ledge = state2.initial

            stack.append(nfa(state1.initial, state2.acceptation))
        elif symbol == '+':
            # Unión
            second = stack.pop()
            first = stack.pop()
            new_initial, new_accepting = state(), state()
            new_accepting.label = "ε"

            l1 = first.initial.label
            l2 = second.initial.label

            first.initial.label, second.initial.label = "ε", "ε"
            new_initial.ledge, new_initial.redge = first.initial, second.initial


            new_first, new_second = state(), state()
            new_first.label, new_second.label = l1, l2
            first.initial.ledge, second.initial.ledge = new_first, new_second
            new_first.ledge, new_second.ledge = new_accepting, new_accepting


            stack.append(nfa(new_initial, new_accepting))

        elif symbol == '*':
            state1 = stack.pop()
            new_initial, new_accepting = state(), state()
            new_accepting.label = "ε"

            new_initial.ledge, new_initial.redge = state1.initial, new_accepting

            state1.acceptation.ledge, state1.acceptation.redge = state1.initial, new_accepting

            stack.append(nfa(new_initial, new_accepting))

    if len(stack) != 1:
        raise ValueError("Expresión no válida")

    return stack.pop()

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
        dot.node(state_name, shape='circle', style='bold' if state.acceptation else '')

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

