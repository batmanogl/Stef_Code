def mini_calculator():
    print("Welcome to the Mini Calculator App!")
    print("Instructions: Enter two numbers and choose an arithmetic operator (+, -, *, /, ^).")
    print("Note: Use the '.' symbol for decimal numbers.\n")
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        operator = input("Enter an arithmetic operator (+, -, *, /): ")
        
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                print("Error: Division by zero is not allowed.")
                return
            result = num1 / num2
        elif operator == '^':
            result = num1 ** num2
        else:
            print("Invalid operator! Please use +, -, *, or /.")
            return
        
        print(f"Result: {num1} {operator} {num2} = {round(result, 5)}")
    except ValueError:
        print("Invalid input! Please enter numeric values.")
        
if __name__ == "__main__":
    mini_calculator()
