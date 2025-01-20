import random

def generate_secret_number():
    # Generate a random 4-digit number with unique digits
    digits = list(range(10))
    random.shuffle(digits)
    return ''.join(map(str, digits[:4]))

def validate_input(number):
    # Validate that input is a 4-digit number with unique digits
    if not number.isdigit() or len(number) != 4:
        return False
    return len(set(number)) == 4

def get_bulls_and_cows(secret, guess):
    # Calculate number of bulls and cows
    bulls = 0
    cows = 0
    
    for i in range(4):
        if secret[i] == guess[i]:
            bulls += 1
    
    common = len(set(secret) & set(guess))
    cows = common - bulls
    
    return bulls, cows

def display_history(history, is_first=False):
    # Display guess history
    if is_first:
        print("\nGuess History:")
        print("No.  Guess   Result")
        print("-" * 20)
    
    if history:
        guess, bulls, cows = history[-1]
        print(f"{len(history):2d}.   {guess}   {bulls}B {cows}C")

def main():
    # Main game function
    print("Welcome to Bulls and Cows game!")
    print("Try to guess a 4-digit number with unique digits.")
    
    secret = generate_secret_number()
    attempts = 0
    history = []
    first_display = True
    
    while True:
        guess = input("Enter your guess: ")
        
        if not validate_input(guess):
            print("Invalid input! Please enter a 4-digit number with unique digits.")
            continue
        
        attempts += 1
        bulls, cows = get_bulls_and_cows(secret, guess)
        
        history.append((guess, bulls, cows))

        display_history(history, first_display)
        first_display = False
        
        if bulls == 4:
            print(f"Congratulations! You won in {attempts} attempts.")
            print(f"The correct answer was: {secret}")
            break

if __name__ == "__main__":
    main()
