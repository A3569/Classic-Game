import random

def read_word_list(filename):
    # Read list of valid 4-letter isogram words from file
    with open(filename, 'r') as f:
        words = [word.strip().lower() for word in f.readlines()]
    return words

def generate_secret_word(word_list):
    # Generate a random 4-letter word from the list
    return random.choice(word_list)

def validate_input(guess, word_list):
    # Validate that input is a valid 4-letter word from the list
    if guess.lower() not in word_list:
        print("Error: Word not found in word list!")
        return False
    
    # Check for repeated letters
    if len(set(guess)) != len(guess):
        print("Error: Word contains repeated letters!")
        return False
        
    return True

def get_bulls_and_cows(secret, guess):
    # Calculate number of bulls and cows
    bulls = 0
    cows = 0

    secret = secret.lower()
    guess = guess.lower()
    
    # Check for bulls
    for i in range(len(secret)):
        if secret[i] == guess[i]:
            bulls += 1
    
    # Check for cows
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
    print("Welcome to Word Bulls and Cows game!")
    print("Try to guess a 4-letter word. Each letter can only be used once.")
    
    word_list = read_word_list("Four-letter isograms.txt")
    secret = generate_secret_word(word_list)
    attempts = 0
    history = []
    first_display = True
    
    while True:
        guess = input("Enter your guess: ")
        
        if validate_input(guess, word_list):
            attempts += 1
            bulls, cows = get_bulls_and_cows(secret, guess)
            
            history.append((guess, bulls, cows))

            display_history(history, first_display)
            first_display = False
            
            if bulls == 4:
                print(f"Congratulations! You won in {attempts} attempts.")
                print(f"The correct word was: {secret}")
                break
        else:
            continue

if __name__ == "__main__":
    main()
