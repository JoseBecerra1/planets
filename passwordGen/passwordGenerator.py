import random
import string

def generate_random_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Define the desired length for the random password
password_length = 12

# Generate a random password
random_password = generate_random_password(password_length)

print(f"Random Password: {random_password}")

