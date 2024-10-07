# A simple Python program that calculates the factorial of a number

# Function to calculate factorial
def factorial(n):
    if n < 0:
        return "Factorial is not defined for negative numbers."
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

# Main part of the program
def main():
    try:
        # Ask the user for a number
        number = int(input("Enter a number to calculate its factorial: "))

        # Call the factorial function
        fact = factorial(number)

        # Output the result
        print(f"The factorial of {number} is: {fact}")
    except ValueError:
        print("Please enter a valid integer.")

# Run the program
if __name__ == "__main__":
    main()
