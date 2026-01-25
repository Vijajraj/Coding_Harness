import random

secret = random.randint(1, 10)   
attempts = 0

while True:
    guess = int(input("Guess the number (1-10): "))
    attempts += 1

    if guess == secret:
        print("Correct! You win!")
        print("Attempts:", attempts)
        break
    elif guess < secret:
        print("Too low. Try again!")
    else:
        print("Too high. Try again!")
