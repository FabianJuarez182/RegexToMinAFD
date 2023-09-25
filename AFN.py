import re

from graphviz import Digraph
def alphanum(a):
    return a.isalpha() or a.isnumeric() or a == "ε"

class state:
    label, ledge, redge = None, None, None

class nfa:

    def __init__(self, initial, acceptation):
        self.initial, self.acceptation = initial, acceptation




def postfix_to_nfa(regex):

    # keys=list(set(re.sub('[^A-Za-z0-9]+', '', regex)+'e'))

    # s=[];stack=[];start=0;end=1

    # counter=-1;c1=0;c2=0

    # for i in regex:
    #     if i in keys:
    #         counter=counter+1;c1=counter;counter=counter+1;c2=counter
    #         s.append({});s.append({})
    #         stack.append([c1,c2])
    #         s[c1][i]=c2
    #     elif i=='*':
    #         r1,r2=stack.pop()
    #         counter=counter+1;c1=counter;counter=counter+1;c2=counter
    #         s.append({});s.append({})
    #         stack.append([c1,c2])
    #         s[r2]['e']=(r1,c2);s[c1]['e']=(r1,c2)
    #         if start==r1:start=c1 
    #         if end==r2:end=c2 
    #     elif i=='.':
    #         r11,r12=stack.pop()
    #         r21,r22=stack.pop()
    #         stack.append([r21,r12])
    #         s[r22]['e']=r11
    #         if start==r11:start=r21 
    #         if end==r22:end=r12 
    #     else:
    #         counter=counter+1;c1=counter;counter=counter+1;c2=counter
    #         s.append({});s.append({})
    #         r11,r12=stack.pop()
    #         r21,r22=stack.pop()
    #         stack.append([c1,c2])
    #         s[c1]['e']=(r21,r11); s[r12]['e']=c2; s[r22]['e']=c2
    #         if start==r11 or start==r21:start=c1 
    #         if end==r22 or end==r12:end=c2

    # return s

    stack = []

    for symbol in regex:
        if alphanum(symbol):
            # Crear un nuevo estado para el símbolo
            new_accepting, new_initial = state(), state()

            new_initial.label, new_initial.ledge = symbol, new_accepting

            

            stack.append(nfa(new_initial, new_accepting))
            
        elif symbol == '^':
            # Concatenación
            state2, state1 = stack.pop(), stack.pop()
            state1.acceptation = state2
            lastf, lasts = None, None
            l1 = state1.initial.label

            if l1 is None:
                l1 = state1.initial.ledge

                while l1 is not None:
                    l1 = l1.ledge
                    if l1:
                        lastf = l1                
                l1 = lastf.label

            if lastf:
                lastf.ledge = state2.initial.ledge
                lastf.redge = state2.initial.redge
                if lastf.ledge:
                    lastf.ledge.label = state2.initial.label
                if lastf.redge:
                    lastf.redge.label = state2.initial.label
                
            else:
                state1.ledge = state2.initial.ledge
                state1.redge = state2.initial.redge
                if state1.ledge:
                    state1.ledge.label = state2.initial.label
                if state1.redge:
                    state1.redge.label = state2.initial.label

            stack.append(nfa(state1.initial, state2.acceptation))
        elif symbol == '+':
            # Unión
            second = stack.pop()
            first = stack.pop()
            new_initial, new_accepting = state(), state()
            lastf, lasts = None, None
            new_accepting.label = "ε"

            l1 = first.initial.label

            if l1 is None:
                l1 = first.initial.ledge

                while l1 is not None:
                    l1 = l1.ledge
                    if l1:
                        lastf = l1
                
                l1 = lastf.label

            l2 = second.initial.label

            if l2 is None:
                l2 = second.initial.ledge

                while l2 is not None:
                    l2 = l2.ledge
                    if l2:
                        lasts = l2
                
                l2 = lasts.label

            first.initial.label, second.initial.label = "ε", "ε"
            new_initial.ledge, new_initial.redge = first.initial, second.initial


            new_first, new_second = state(), state()
            if l1 != "ε":
                new_first.label = l1
                new_first.ledge = new_accepting
            else:
                new_first.label = "ε"
            if l2 != "ε":
                new_second.label = l2
                new_second.ledge = new_accepting
            else:
                new_second.label = "ε"
            if lastf and lasts:
                lastf.ledge, lasts.ledge = new_first, new_second
            elif lastf:
                lastf.ledge, second.initial.ledge = new_first, new_second
            elif lasts:
                first.initial.ledge , lasts.ledge = new_first, new_second
            else:
                first.initial.ledge, second.initial.ledge = new_first, new_second

            


            stack.append(nfa(new_initial, new_accepting))

        elif symbol == '*':
            state1 = stack.pop()
            new_initial, new_accepting, new_transition = state(), state(), state()

            new_accepting.label = "ε"
            new_transition.label = "ε"

            new_initial.ledge, new_initial.redge = new_transition, new_accepting

            new_transition.ledge = state1.initial

            state1.initial.ledge, state1.initial.redge = new_accepting, new_transition

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

