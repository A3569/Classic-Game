import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

# Define grid size and game parameters
GRID_SIZE = 40
GRID_WIDTH = 22
GRID_HEIGHT = 12
WINDOW_WIDTH = GRID_WIDTH * GRID_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * GRID_SIZE + 60

# Create game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake')

# Snake class to manage snake behavior
class Snake:
    def __init__(self):
        # Random starting position
        self.body = [(random.randint(2, GRID_WIDTH-3), random.randint(2, GRID_HEIGHT-3))]
        # Random starting direction
        self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        self.grow = False 
        
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        self.grow = False
        
    def check_collision(self):
        head = self.body[0]
        return (head[0] < 0 or head[0] >= GRID_WIDTH or
                head[1] < 0 or head[1] >= GRID_HEIGHT or
                head in self.body[1:])

# Main game class
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = self.spawn_food()
        self.score = 0
        self.speed = 3
        
    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH-1), 
                   random.randint(0, GRID_HEIGHT-1))
            if food not in self.snake.body:
                return food
    
    def draw_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pygame.draw.rect(screen, GRAY, 
                               (x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
    
    def main_menu(self):
        while True:
            screen.fill(BLACK)
            self.draw_grid()
            font = pygame.font.Font(None, 74)
            
            # Add welcome text
            welcome_text = font.render('Welcome to Snake', True, WHITE)
            start_text = font.render('Start Game', True, GREEN)
            exit_text = font.render('Exit Game', True, RED)
            
            welcome_rect = welcome_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4))
            start_rect = start_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            exit_rect = exit_text.get_rect(center=(WINDOW_WIDTH//2, 3*WINDOW_HEIGHT//4))
            
            screen.blit(welcome_text, welcome_rect)
            screen.blit(start_text, start_rect)
            screen.blit(exit_text, exit_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if start_rect.collidepoint(mouse_pos):
                        return True
                    if exit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
    
    def game_over_screen(self):
        screen.fill(BLACK)
        self.draw_grid()
        font = pygame.font.Font(None, 74)
        score_text = font.render(f'Final score: {self.score}', True, WHITE)
        return_text = font.render('Return to Menu', True, GREEN)
        
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3))
        return_rect = return_text.get_rect(center=(WINDOW_WIDTH//2, 2*WINDOW_HEIGHT//3))
        
        screen.blit(score_text, score_rect)
        screen.blit(return_text, return_rect)
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if return_rect.collidepoint(event.pos):
                        return
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            if not self.main_menu():
                break
                
            # Reset game state
            self.snake = Snake()
            self.food = self.spawn_food()
            self.score = 0
            self.speed = 3
            
            while True:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                            self.snake.direction = (0, -1)
                        if event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                            self.snake.direction = (0, 1)
                        if event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                            self.snake.direction = (-1, 0)
                        if event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                            self.snake.direction = (1, 0)
                        if event.key == pygame.K_ESCAPE:
                            return
                
                self.snake.move()
                
                # Check game over conditions
                if self.snake.check_collision():
                    self.game_over_screen()
                    break
                
                # Handle food collection
                if self.snake.body[0] == self.food:
                    self.snake.grow = True
                    self.food = self.spawn_food()
                    self.score += 30
                    if self.speed < 20:
                        self.speed += 0.1
                
                # Check win condition
                if len(self.snake.body) == GRID_WIDTH * GRID_HEIGHT:
                    self.game_over_screen()
                    break
                
                # Draw game elements
                screen.fill(BLACK)
                self.draw_grid()
                
                # Draw food
                pygame.draw.rect(screen, RED, 
                               (self.food[0]*GRID_SIZE, self.food[1]*GRID_SIZE, 
                                GRID_SIZE-2, GRID_SIZE-2))
                
                # Draw snake
                for segment in self.snake.body:
                    pygame.draw.rect(screen, GREEN,
                                   (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE,
                                    GRID_SIZE-2, GRID_SIZE-2))
                
                # Display score
                font = pygame.font.Font(None, 36)
                score_text = font.render(f'Score: {self.score}', True, WHITE)
                screen.blit(score_text, (10, WINDOW_HEIGHT - 40))
                
                pygame.display.flip()
                clock.tick(self.speed)

if __name__ == '__main__':
    game = Game()
    game.run()
