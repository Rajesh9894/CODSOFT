def calculator():
    print("Simple Calculator")
    print("Operations: +, -, *, /")

    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        operation = input("Enter operation (+, -, *, /): ")

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                print("Error: Division by zero")
                return
            result = num1 / num2
        else:
            print("Invalid operation")
            return

        print(f"Result: {result}")
    except ValueError:
        print("Invalid input. Please enter numbers.")

if __name__ == "__main__":
    calculator()
