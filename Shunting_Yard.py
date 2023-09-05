def alphanum(a):
    return a.isalpha() or a.isnumeric() or a == "ε"


def shunting_yard(regex):
    precedence = {'*': 3, '^': 2, '+': 1}
    output = []
    operator_list = ["*", "+", "^", "(", ")"]
    operator_stack = []
    cont = -1
    sumflag = False
    contsum = 0

    for char in regex:
        cont += 1
        if alphanum(char):
            if len(operator_stack) != 0 and len(operator_stack) >= 2:
                if operator_stack[-2] != "(":
                    if operator_stack[-1] == "*":
                        output.append(operator_stack.pop())
                    if operator_stack[-1] == "+":
                        output.append(operator_stack.pop())
            output.append(char)
            if sumflag:
                contsum += 1
            if len(output) >= 2:
                if (alphanum(output[-2])) and len(operator_stack) == 0:
                    output.append("^")
                elif (output[-2] in operator_list) and len(operator_stack) == 0:
                    if regex[cont+1] == "*" :
                        output.append("*")
                        output.append("^")
                        break
                    else:
                        output.append("^")
                elif operator_stack[-1] == "(" and len(operator_stack) == 1:
                    if alphanum(output[-2]):
                        if operator_stack[-1] != "(":
                            output.append("^")
                    elif (output[-2] in operator_list):
                        if operator_stack[-1] != "(":
                            output.append("^")
                elif operator_stack[-1] == "+" and len(operator_stack) == 1:
                    output.append(operator_stack.pop())
            if contsum == 2:
                if cont < len(regex) - 1:
                    if regex[cont+1] != ")":
                        if operator_stack:
                            output.append(operator_stack.pop())
                        contsum = 0
                        sumflag = False
        elif char in "+":
            operator_stack.append(char)
            contsum += 1 
            sumflag == True
        elif char == "*":
            if operator_stack:
                if operator_stack[-1] == "(":
                    output.append("*")
                elif (alphanum(output[-1])) or ((alphanum(output[-2])) and (output[-1] == "^" or output[-1] == "+" )):
                    output.append("*")
                elif output[-1] in "^+" and alphanum(output[-2]):
                    output.append("*")
        elif char == "(":
            operator_stack.append(char)
        elif char == ")":
            while operator_stack and operator_stack[-1] != "(":
                output.append(operator_stack.pop())
            if not operator_stack or operator_stack[-1] != "(":
                raise ValueError("Error: Paréntesis no cerrado.")
            operator_stack.pop()
    if output[-1] != "^":
        a = next((x for x in range(len(output)) if output[x] == "^"), None)
        if a and  a > 0:
                output.append("^")
            
        
            
        

            
    while operator_stack:
        if operator_stack[-1] == "(":
            
            raise ValueError("Error: "+ regex +" Expresion invalida, parentesis no balanceado.")
        output.append(operator_stack.pop())

    return ''.join(output)

try:
    postfix_expression = shunting_yard("((a+b)*+a)aaa(a+b)")
    print("Expresión regular en notación postfix:", postfix_expression)
except ValueError as e:
    print(e)