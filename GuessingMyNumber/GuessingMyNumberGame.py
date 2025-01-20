import random

# Generate passcode
number = random.randint(1, 100)

# Create variables to store latest range
min = 0
max = 100
max_attempts = 10
player_attempts = 0

# Player starts guessing
while player_attempts < max_attempts:
    guess = int(input(f'The range is between {min}~{max}, please guess the number:'))
    player_attempts += 1

    if guess > max or guess < min:
        print('Invalid number, please try again.')

    elif guess == number:
        print('Correct guess, You won.')
        print(f'The answer is: {number}')
        break

    elif guess > number:
        print('Number too large')
        max = guess

    else:
        print('Number too small')
        min = guess
    
    if player_attempts == max_attempts:
        print('You lost.')
        print(f'The answer is: {number}')
        break
