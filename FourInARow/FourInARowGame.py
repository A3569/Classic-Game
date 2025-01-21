import pygame
import random
import sys

# Creates an empty 6x7 game board represented as a 2D list
def create_board():
    return [[0 for _ in range(7)] for _ in range(6)]

# Places a piece (1 for player, 2 for AI) at the specified row and column
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Checks if a column is valid for placing a piece (not full and within bounds)
def is_valid_location(board, col):
    if col < 0 or col >= 7:
        return False
    return board[0][col] == 0

# Returns the next available row in a column, or None if column is full
def get_next_open_row(board, col):
    if col < 0 or col >= 7:
        return None
    for r in range(5, -1, -1):
        if board[r][col] == 0:
            return r
    return None

# Checks if there are three pieces in a row for a given player
# Returns True/False and the position to block if found
def check_three_in_a_row(board, piece):
    # Check horizontal
    for r in range(6):
        for c in range(5):
            if board[r][c:c+3] == [piece]*3:
                return True, r, c+3
                
    # Check vertical  
    for c in range(7):
        for r in range(4):
            if [board[r+i][c] for i in range(3)] == [piece]*3:
                return True, r+3, c
            
    # Check diagonal (positive slope)
    for c in range(4):
        for r in range(3):
            if (board[r][c] == piece and 
                board[r+1][c+1] == piece and 
                board[r+2][c+2] == piece):
                return True, r+3, c+3
                
    # Check diagonal (negative slope)
    for c in range(4):
        for r in range(5, 2, -1):
            if (board[r][c] == piece and 
                board[r-1][c+1] == piece and 
                board[r-2][c+2] == piece):
                return True, r-3, c+3
                
    return False, None, None

# Checks if a player has won by getting 4 in a row in any direction
def winning_move(board, piece):
    # Check horizontal
    for c in range(4):
        for r in range(6):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical
    for c in range(7):
        for r in range(3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check diagonal (positive slope)
    for c in range(4):
        for r in range(3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check diagonal (negative slope)
    for c in range(4):
        for r in range(3, 6):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

# Checks if placing a piece in a column would result in a win
def check_potential_win(board, piece, col):
    if col < 0 or col >= 7:
        return False
    
    row = get_next_open_row(board, col)
    if row is not None:
        temp_board = [row[:] for row in board]
        drop_piece(temp_board, row, col, piece)
        return winning_move(temp_board, piece)
    return False

# Checks if the board is completely full (draw condition)
def is_board_full(board):
    return all(board[0][col] != 0 for col in range(7))

# AI logic for choosing next move
def ai_move(board):
    # First check if AI can win in next move
    for col in range(7):
        if is_valid_location(board, col):
            if check_potential_win(board, 2, col):
                return col

    # Then check if player can win in next move and block it
    for col in range(7):
        if is_valid_location(board, col):
            if check_potential_win(board, 1, col):
                return col

    # Then check if player has three in a row to block
    has_three, row, col = check_three_in_a_row(board, 1)
    if has_three and col < 7 and col >= 0:  # Add bounds check
        if is_valid_location(board, col):
            return col
                
    # Otherwise make random move
    valid_locations = [col for col in range(7) if is_valid_location(board, col)]
    if valid_locations:
        return random.choice(valid_locations)
    return None

# Draws the game board on the screen using pygame
def draw_board(screen, board):
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    
    for c in range(7):
        for r in range(6):
            pygame.draw.rect(screen, BLUE, (c*100, r*100+100, 100, 100))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (c*100+50, r*100+150), 40)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c*100+50, r*100+150), 40)
            else:
                pygame.draw.circle(screen, YELLOW, (c*100+50, r*100+150), 40)
    pygame.display.update()

# Draws a button with text on the screen
def draw_button(screen, text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.SysFont("monospace", 30)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
    screen.blit(text_surface, text_rect)

# Main menu interface with game mode selection
def main_menu():
    pygame.init()
    WIDTH = 700
    HEIGHT = 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Four in a Row')
    
    while True:
        screen.fill((255, 255, 255))
        draw_button(screen, "Player vs AI", 150, 200, 400, 80, (0, 255, 0))
        draw_button(screen, "Player vs Player", 150, 300, 400, 80, (0, 255, 0))
        draw_button(screen, "Exit", 150, 400, 400, 80, (255, 0, 0))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 150 <= mouse_pos[0] <= 550:
                    if 200 <= mouse_pos[1] <= 280:
                        play_game(screen, True)  # AI mode
                    elif 300 <= mouse_pos[1] <= 380:
                        play_game(screen, False)  # 2 Player mode
                    elif 400 <= mouse_pos[1] <= 480:
                        pygame.quit()
                        sys.exit()

# Main game loop handling player moves, AI moves, and win conditions
def play_game(screen, ai_mode):
    WIDTH = 700
    HEIGHT = 700
    board = create_board()
    game_over = False
    turn = 0
    
    draw_board(screen, board)
    pygame.display.update()
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEMOTION and not game_over:
                pygame.draw.rect(screen, (0,0,0), (0,0, WIDTH, 100))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, (255,0,0), (posx, 50), 40)
                elif not ai_mode and turn == 1:
                    pygame.draw.circle(screen, (255,255,0), (posx, 50), 40)
                pygame.display.update()
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                posx = event.pos[0]
                col = posx//100
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    if row is not None:
                        if turn == 0:
                            drop_piece(board, row, col, 1)
                            if winning_move(board, 1):
                                pygame.draw.rect(screen, (0,0,0), (0,0, WIDTH, 100))
                                font = pygame.font.SysFont("monospace", 75)
                                label = font.render("Player 1 wins!!", 1, (255,0,0))
                                screen.blit(label, (40,10))
                                game_over = True
                            turn = 1
                        elif not ai_mode and turn == 1:
                            drop_piece(board, row, col, 2)
                            if winning_move(board, 2):
                                pygame.draw.rect(screen, (0,0,0), (0,0, WIDTH, 100))
                                font = pygame.font.SysFont("monospace", 75)
                                label = font.render("Player 2 wins!!", 1, (255,255,0))
                                screen.blit(label, (40,10))
                                game_over = True
                            turn = 0
                        draw_board(screen, board)
        
        # AI's turn
        if ai_mode and turn == 1 and not game_over:
            col = ai_move(board)
            
            if col is not None and is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                if row is not None:
                    drop_piece(board, row, col, 2)
                    
                    if winning_move(board, 2):
                        pygame.draw.rect(screen, (0,0,0), (0,0, WIDTH, 100))
                        font = pygame.font.SysFont("monospace", 75)
                        label = font.render("AI wins!!", 1, (255,255,0))
                        screen.blit(label, (40,10))
                        game_over = True
                        
                    turn = 0
                    draw_board(screen, board)
        
        # Check if the game is full and no one wins
        if is_board_full(board) and not game_over:
            pygame.draw.rect(screen, (0,0,0), (0,0, WIDTH, 100))
            font = pygame.font.SysFont("monospace", 75)
            label = font.render("Draw!", 1, (255,255,255))
            screen.blit(label, (40,10))
            game_over = True
            draw_board(screen, board)
            
        if game_over:
            pygame.time.wait(3000)
            return

if __name__ == "__main__":
    main_menu()
