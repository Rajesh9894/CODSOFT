import random
import string

def generate_password(length):
    # Use a combination of uppercase, lowercase, digits, and punctuation
    characters = string.ascii_letters + string.digits + string.punctuation
    # Generate password
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    print("Welcome to the Password Generator!")

    # Prompt for password length
    while True:
        try:
            length = int(input("Enter the desired password length: "))
            if length <= 0:
                print("Length must be a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Generate and display password
    password = generate_password(length)
    print(f"Generated Password: {password}")

if __name__ == "__main__":
    main()
