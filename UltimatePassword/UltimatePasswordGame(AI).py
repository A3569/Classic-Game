import random

# Generate a random password between 0 and 100
password = random.randint(0, 100)

# Initialize the range and attempts counter
lower_bound = 0
upper_bound = 100
player_attempts = 0
ai_attempts = 0
max_attempts = 10

print("Welcome to The Ultimate password! You'll compete against an AI to try not to find the password first.")
print("You'll take turns guessing - you go first!")
print(f"Current range: {lower_bound}-{upper_bound}")

while player_attempts < max_attempts and ai_attempts < max_attempts:
    # Player's turn
    try:
        guess = int(input(f"\nYour turn! Enter your guess between {lower_bound} and {upper_bound} ({max_attempts - player_attempts} attempts left): "))
        if guess < lower_bound or guess > upper_bound:
            raise ValueError(f"Error: Your guess must be between {lower_bound} and {upper_bound}")
    except ValueError as e:
        print(str(e))
        continue
        
    player_attempts += 1
    print(f"\nYou guessed: {guess}")
    
    # Check player's guess
    if guess == password:
        print(f"Oh no! YOU found the password ({password}). You lose!")
        break
    elif guess > password:
        upper_bound = guess
        print(f"New range: {lower_bound}-{upper_bound}")
    else:
        lower_bound = guess
        print(f"New range: {lower_bound}-{upper_bound}")
    
    # Check for deadlock after player's move
    if lower_bound + 2 == upper_bound:
        print(f"The AI can only guess {upper_bound - 1}, so you win!")
        break
        
    # AI's turn
    print("\nAI's turn...")
    ai_guess = random.randint(lower_bound, upper_bound)
    ai_attempts += 1
    print(f"AI guesses: {ai_guess}")
    
    # Check AI's guess
    if ai_guess == password:
        print(f"The AI found the password ({password}). You win!")
        break
    elif ai_guess > password:
        upper_bound = ai_guess
        print(f"New range: {lower_bound}-{upper_bound}")
    else:
        lower_bound = ai_guess
        print(f"New range: {lower_bound}-{upper_bound}")
    
    # Check for deadlock after AI's move
    if lower_bound + 2 == upper_bound:
        print(f"You can only guess {upper_bound - 1}, so you lose!")
        break

if (player_attempts == max_attempts and ai_attempts == max_attempts) and guess != password and ai_guess != password:
    print(f"\nDraw! Both of you used all {max_attempts} attempts. The password was {password}")
