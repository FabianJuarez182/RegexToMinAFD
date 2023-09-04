def shunting_yard(regex):
    precedence = {'*': 3, '^': 2, '+': 1}
    output = []
    operator_list = ["*", "+", "^", "(", ")"]
    operator_stack = []
    cont = -1

    for char in regex:
        cont += 1
        if char.isalpha() or char.isnumeric() or char == "ε":
            if len(operator_stack) != 0 and len(operator_stack) >= 2:
                if operator_stack[-2] != "(":
                    if operator_stack[-1] == "*":
                        output.append(operator_stack.pop())
                    if operator_stack[-1] == "+":
                        output.append(operator_stack.pop())
            output.append(char)
            if len(output) >= 2:
                if (output[-2].isalpha() or output[-2].isnumeric() or output[-2] == "ε") and len(operator_stack) == 0:
                    output.append("^")
                elif (output[-2] in operator_list) and len(operator_stack) == 0:
                    if regex[cont+1] == "*" :
                        output.append("*")
                        output.append("^")
                        break
                    else:
                        output.append("^")
                elif operator_stack[-1] == "+" and len(operator_stack) == 1:
                    output.append(operator_stack.pop())
        elif char in "+":
            operator_stack.append(char) 
        elif char == "*":
            if operator_stack:
                if operator_stack[-1] == "(":
                    output.append("*")
            elif (output[-1].isnumeric() or output[-1].isalpha()) or ((output[-2].isnumeric() or output[-2].isalpha()) and (output[-1] == "^" or output[-1] == "+" )  ):
                output.append("*")
        elif char == "(":
            operator_stack.append(char)
        elif char == ")":
            while operator_stack and operator_stack[-1] != "(":
                output.append(operator_stack.pop())
            operator_stack.pop()
        
    
    while operator_stack:
        output.append(operator_stack.pop())

    return ''.join(output)

postfix_expression = shunting_yard("(a+b)*abc*")
print("Expresión regular en notación postfix:", postfix_expression)

postfix_expression = shunting_yard("(a+b)*+aaa(a+b)")

print("Expresión regular en notación postfix:", postfix_expression)