import random
import json
from time import sleep
from enum import Enum

# Initialize game board with given size (default 10x10)
def initialise_board(size=10):
    return [[None] * size for _ in range(size)]

# Create dictionary of battleships with their sizes
def create_battleships(filename="battleships.txt"):
    battleships = {
        "Aircraft_Carrier": 5,
        "Battleship": 4, 
        "Cruiser": 3,
        "Submarine": 3,
        "Destroyer": 2
    }
    return battleships

# Main function to place ships on the board
def place_battleships(board, ships, algorithm='random'):
    # Check if ship placement is within bounds and not overlapping other ships
    def is_valid_placement(row, col, size, orientation, board):
        if orientation == 'h':
            if col + size > len(board[0]):
                return False
            
            for i in range(max(0, row-1), min(len(board), row+2)):
                for j in range(max(0, col-1), min(len(board[0]), col+size+1)):
                    if board[i][j] is not None:
                        return False
            return True
        
        elif orientation == 'v':
            if row + size > len(board):
                return False

            for i in range(max(0, row-1), min(len(board), row+size+1)):
                for j in range(max(0, col-1), min(len(board[0]), col+2)):
                    if board[i][j] is not None:
                        return False
            return True
        return False
    
    # Place ship horizontally on board
    def place_ship_horizontal(ship, row, col, size, board):
        for i in range(size):
            board[row][col + i] = ship
        return board

    # Place ship vertically on board
    def place_ship_vertical(ship, row, col, size, board):
        for i in range(size):
            board[row + i][col] = ship
        return board

    # Handle manual ship placement by user
    def place_ship_manual(ship, size, board):
        while True:
            print(f"\nPlacing {ship} (size: {size})")
            print_board(board)
            try:
                h_orientation = int(input("Enter horizontal position (0-9): "))
                v_orientation = int(input("Enter vertical position (0-9): "))
                direction = input("Enter direction (h for horizontal, v for vertical): ").lower()
                
                if direction not in ['h', 'v']:
                    print("Direction must be 'h' for horizontal or 'v' for vertical")
                    continue
                    
                if 0 <= h_orientation < len(board) and 0 <= v_orientation < len(board):
                    if is_valid_placement(v_orientation, h_orientation, size, direction, board):
                        if direction == 'h':
                            return place_ship_horizontal(ship, v_orientation, h_orientation, size, board)
                        else:
                            return place_ship_vertical(ship, v_orientation, h_orientation, size, board)
                    else:
                        print("Invalid placement. Ships cannot overlap or be adjacent to other ships")
                else:
                    print("Coordinates must be between 0 and 9")
            except ValueError:
                print("Please enter valid numbers")

    # Handle random ship placement
    def place_ships_random(ships, board):
        temp_board = [row[:] for row in board]
        
        for ship, size in ships.items():
            placed = False
            attempts = 0
            max_attempts = 100
            
            while not placed and attempts < max_attempts:
                orientation = random.choice(['h', 'v'])
                
                if orientation == 'h':
                    row = random.randint(0, len(board) - 1)
                    col = random.randint(0, len(board[0]) - size)
                else:
                    row = random.randint(0, len(board) - size)
                    col = random.randint(0, len(board[0]) - 1)
                
                if is_valid_placement(row, col, size, orientation, temp_board):
                    if orientation == 'h':
                        temp_board = place_ship_horizontal(ship, row, col, size, temp_board)
                    else:
                        temp_board = place_ship_vertical(ship, row, col, size, temp_board)
                    placed = True
                    print(f"Successfully placed {ship}")
                
                attempts += 1
            
            if not placed:
                print(f"Failed to place {ship} after {max_attempts} attempts")
                return None
        
        return temp_board

    # Main placement logic based on algorithm choice
    if algorithm == 'random':
        placed_board = place_ships_random(ships, board)
        while placed_board is None:
            placed_board = place_ships_random(ships, board)
        return placed_board
    else:
        placement_choice = input("\nDo you want random placement or custom placement? (random/custom): ").lower()
        if placement_choice == 'random':
            placed_board = place_ships_random(ships, board)
            while placed_board is None:
                placed_board = place_ships_random(ships, board)
            return placed_board
        else:
            for ship, size in ships.items():
                board = place_ship_manual(ship, size, board)
            return board

# Handle attack on a position
def attack(coordinates, board, battleships):
    row, col = coordinates
    if board[row][col] == 'X' or board[row][col] == 'O':
        print("This spot has already been attacked! Please choose another spot.")
        return None
    hit = board[row][col] is not None
    if hit:
        ship = board[row][col]
        battleships[ship] -= 1
        board[row][col] = 'O'
    else:
        board[row][col] = 'X'
    return hit

# Generate random attack coordinates
def generate_attack(size):
    return random.randint(0, size-1), random.randint(0, size-1)

# Print the game board
def print_board(board, hide_ships=False):
    print("  " + "   ".join(str(i) for i in range(len(board))))
    for i, row in enumerate(board):
        print(f"{i} ", end="")
        for cell in row:
            if cell == 'X':
                print("X", end="   ")
            elif cell == 'O':
                print("O", end="   ")
            elif cell is None:
                print(".", end="   ")
            elif hide_ships:
                print(".", end="   ")
            else:
                print("🚢", end=" ")
        print()

def main():
    board_size = 10
    player_board = initialise_board(board_size)
    ai_board = initialise_board(board_size)
    
    ships = create_battleships()
    player_ships = ships.copy()
    ai_ships = ships.copy()
    
    # Place ships manually for player and randomly for AI
    print("\nPlace your ships:")
    player_board = place_battleships(player_board, player_ships, algorithm='custom')
    ai_board = place_battleships(ai_board, ai_ships, algorithm='random')
    
    print("\nYour board:")
    print_board(player_board)
    print("\nAI board:")
    print_board(ai_board, hide_ships=True)
    
    while True:
        while True:
            try:
                x = int(input("\nEnter x coordinate (0-9): "))
                y = int(input("Enter y coordinate (0-9): "))
                if 0 <= x < board_size and 0 <= y < board_size:
                    break
                print("Coordinates must be between 0 and 9")
            except ValueError:
                print("Please enter valid numbers")
        
        hit = attack((y, x), ai_board, ai_ships)
        if hit is None:
            continue
        print("Hit!" if hit else "Miss!")
        
        if all(v == 0 for v in ai_ships.values()):
            print("\nCongratulations! You win!")
            break
            
        print("\nAI's turn...")
        sleep(1)
        while True:
            ai_x, ai_y = generate_attack(board_size)
            if player_board[ai_y][ai_x] != 'X' and player_board[ai_y][ai_x] != 'O':
                break
        ai_hit = attack((ai_y, ai_x), player_board, player_ships)
        print(f"AI attacks position ({ai_x}, {ai_y})")
        print("AI Hit!" if ai_hit else "AI Miss!")
        
        print("\nYour board:")
        print_board(player_board)
        print("\nAI board:")
        print_board(ai_board, hide_ships=True)
        
        if all(v == 0 for v in player_ships.values()):
            print("\nGame Over! AI wins!")
            break

if __name__ == '__main__':
    main()
