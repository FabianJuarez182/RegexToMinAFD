from Shunting_Yard import shunting_yard
from AFN import postfix_to_nfa, visualize_nfa
from AFD import AFD
from PIL import Image


def main():
    expression = "((a+b)+c)c"
    chain = ""

    try:
        postfix_expression = shunting_yard(expression)
        print("Expresión regular ingresada:", expression)
        print("Expresión en postfix:", postfix_expression)
        nfa = postfix_to_nfa(postfix_expression)

        print(str(nfa))

        print("Imagen del AFN generada con éxito.")

        # Visualizar el AFN
        #visualize_nfa(nfa)

        # Abrir y mostrar la imagen generada
        #view_image("nfa.png")
        
        dfa = AFD(nfa)
        
        print(dfa)

    except ValueError as e:
        print(e)

def view_image(image_filename):
    img = Image.open(image_filename)
    img.show()

if __name__ == "__main__":
    main()