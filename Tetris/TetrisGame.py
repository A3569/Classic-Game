import pygame
import random
import sys

# Initialization Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Color Definition
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Different colors for Tetriminoes
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
]

# Define the shapes of the Tetriminoes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# Button class for UI elements in the menu and restart button
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Main menu class for the game's starting screen
class MainMenu:
    def __init__(self):
        # Set up the screen and clock
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Welcome to Tetris!')
        self.clock = pygame.time.Clock()
        
        # Create buttons for difficulty levels
        self.easy_button = Button(300, 200, 200, 50, "Easy mode", GREEN)
        self.normal_button = Button(300, 300, 200, 50, "Medium mode", BLUE)
        self.hard_button = Button(300, 400, 200, 50, "Hard mode", RED)
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.easy_button.is_clicked(pos):
                        game = Tetris(30)  # Easy mode
                        game.run()
                    elif self.normal_button.is_clicked(pos):
                        game = Tetris(20)   # Medium mode
                        game.run()
                    elif self.hard_button.is_clicked(pos):
                        game = Tetris(10)   # Hard mode
                        game.run()
            
            self.screen.fill(BLACK)

            # Draw the title
            font = pygame.font.Font(None, 74)
            title = font.render('Welcome to Tetris', True, WHITE)
            self.screen.blit(title, (WINDOW_WIDTH//2 - 150, 100))
            
            # Draw the buttons
            self.easy_button.draw(self.screen)
            self.normal_button.draw(self.screen)
            self.hard_button.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)

# Tetris game class
class Tetris:
    def __init__(self, fall_speed):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.fall_speed = fall_speed
        self.reset_game()
        self.restart_button = Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 50, 200, 50, "New Game", GREEN)

    def reset_game(self):
        self.board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.next_piece = random.choice(SHAPES)
        self.next_color = random.choice(COLORS)
        self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        self.current_piece = self.next_piece
        self.current_color = self.next_color
        self.next_piece = random.choice(SHAPES)
        self.next_color = random.choice(COLORS)
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        
        # End game if the new piece can't be placed
        if not self.valid_move(self.current_piece, self.current_x, self.current_y):
            self.game_over = True

    def valid_move(self, piece, x, y):
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j]:
                    if (x + j < 0 or x + j >= GRID_WIDTH or
                        y + i >= GRID_HEIGHT or
                        (y + i >= 0 and self.board[y + i][x + j])):
                        return False
        return True

    def merge_piece(self):
        for i in range(len(self.current_piece)):
            for j in range(len(self.current_piece[0])):
                if self.current_piece[i][j]:
                    self.board[self.current_y + i][self.current_x + j] = self.current_color

    def rotate_piece(self):
        rows = len(self.current_piece)
        cols = len(self.current_piece[0])
        rotated = [[self.current_piece[rows-1-j][i] for j in range(rows)] for i in range(cols)]
        if self.valid_move(rotated, self.current_x, self.current_y):
            self.current_piece = rotated

    def clear_lines(self):
        lines_cleared = 0
        i = GRID_HEIGHT - 1
        while i >= 0:
            if all(self.board[i]):
                del self.board[i]
                self.board.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
            else:
                i -= 1
                
        # Scoring system based on the number of lines cleared
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 800

    def draw_next_piece(self):
        # Display the next piece on the screen
        font = pygame.font.Font(None, 36)
        next_text = font.render('Next Piece:', True, WHITE)
        self.screen.blit(next_text, (550, 50))
        
        # Draw the next piece
        for i in range(len(self.next_piece)):
            for j in range(len(self.next_piece[0])):
                if self.next_piece[i][j]:
                    pygame.draw.rect(self.screen, self.next_color,
                                   [550 + j * BLOCK_SIZE,
                                    100 + i * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1])

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw the grid lines
        for i in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, GRAY, 
                           (200, i * BLOCK_SIZE),
                           (200 + GRID_WIDTH * BLOCK_SIZE, i * BLOCK_SIZE))
        for j in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, GRAY,
                           (200 + j * BLOCK_SIZE, 0),
                           (200 + j * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
        
        # Draw the game area
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.board[i][j]:
                    pygame.draw.rect(self.screen, self.board[i][j],
                                   [j * BLOCK_SIZE + 200, i * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1])

        # Draw the current piece
        if not self.game_over:
            for i in range(len(self.current_piece)):
                for j in range(len(self.current_piece[0])):
                    if self.current_piece[i][j]:
                        pygame.draw.rect(self.screen, self.current_color,
                                       [(self.current_x + j) * BLOCK_SIZE + 200,
                                        (self.current_y + i) * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1])

        # Draw the score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (50, 50))

        # Draw the next piece
        self.draw_next_piece()

        # Show the game over message if the game is over
        if self.game_over:
            game_over_text = font.render('Game Over!', True, WHITE)
            final_score_text = font.render(f'Final Score: {self.score}', True, WHITE)
            self.screen.blit(game_over_text, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 50))
            self.screen.blit(final_score_text, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2))
            self.restart_button.draw(self.screen)

        pygame.display.flip()

    def run(self):
        fall_time = 0
        
        while True:
            fall_time += 1
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    
                    if not self.game_over:
                        if event.key == pygame.K_LEFT:
                            if self.valid_move(self.current_piece, self.current_x - 1, self.current_y):
                                self.current_x -= 1
                        elif event.key == pygame.K_RIGHT:
                            if self.valid_move(self.current_piece, self.current_x + 1, self.current_y):
                                self.current_x += 1
                        elif event.key == pygame.K_DOWN:
                            if self.valid_move(self.current_piece, self.current_x, self.current_y + 1):
                                self.current_y += 1
                        elif event.key == pygame.K_UP:
                            self.rotate_piece()
                        elif event.key == pygame.K_SPACE:
                            while self.valid_move(self.current_piece, self.current_x, self.current_y + 1):
                                self.current_y += 1
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                    pos = pygame.mouse.get_pos()
                    if self.restart_button.is_clicked(pos):
                        return

            if not self.game_over:
                if fall_time >= self.fall_speed:
                    if self.valid_move(self.current_piece, self.current_x, self.current_y + 1):
                        self.current_y += 1
                    else:
                        self.merge_piece()
                        self.clear_lines()
                        if not self.game_over:
                            self.new_piece()
                    fall_time = 0

            self.draw()
            self.clock.tick(60)

if __name__ == '__main__':
    menu = MainMenu()
    menu.run()
