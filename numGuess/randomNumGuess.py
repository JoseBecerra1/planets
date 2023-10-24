import random

# Generate a random number between 1 and 10
random_number = random.randint(1, 10)

# Initialize variables
guess = None
attempts = 0

print("Welcome to the Random Number Guessing Game!")
print("I'm thinking of a number between 1 and 10. Can you guess what it is?")

while guess != random_number:
    try:
        guess = int(input("Enter your guess: "))
        attempts += 1

        if guess < random_number:
            print("Too low! Try again.")
        elif guess > random_number:
            print("Too high! Try again.")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 10.")

print(f"Congratulations! You guessed the number {random_number} correctly in {attempts} attempts.")

