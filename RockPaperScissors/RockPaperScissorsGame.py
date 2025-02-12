import random
import pygame
import os
import sys

# Initialize Pygame library
pygame.init()

# Define window dimensions and frame rate
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Define color constants using RGB values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)

# Set up the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Welcome to Rock Paper Scissors!")
clock = pygame.time.Clock()

# Function to load game images
def load_images():
    # Get the assets directory path
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    images = {}
    try:
        # Load each game image
        images['scissors'] = pygame.image.load(os.path.join(assets_dir, 'scissors.png'))
        images['paper'] = pygame.image.load(os.path.join(assets_dir, 'paper.png'))
        images['rock'] = pygame.image.load(os.path.join(assets_dir, 'rock.png'))
        
        # Resize all images to 100x100 pixels
        for key in images:
            images[key] = pygame.transform.scale(images[key], (100, 100))
    except pygame.error:
        print("Couldn't load images. Using colored rectangles instead.")
        # Create fallback colored rectangles if images can't be loaded
        surf = pygame.Surface((100, 100))
        surf.fill(BLUE)
        images = {
            'scissors': surf,
            'paper': surf,
            'rock': surf
        }
    return images

# Button class for interactive elements
class Button:
    def __init__(self, x, y, width, height, text, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.image = image
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        # Draw button background with hover effect
        color = GRAY if self.is_hovered else WHITE
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        # Draw button image if available
        if self.image:
            image_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, image_rect)
        
        # Draw button text
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        # Handle mouse hover and click events
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

# Main game class
class Game:
    def __init__(self):
        self.images = load_images()
        self.choices = ['scissors', 'paper', 'rock']
        self.buttons = [
            Button(50 + i*250, 450, 200, 100, choice, self.images[choice])
            for i, choice in enumerate(self.choices)
        ]
        # Initialize game state variables
        self.user_choice = None
        self.computer_choice = None
        self.result = None
        self.font = pygame.font.Font(None, 48)
        self.play_again_button = Button(300, 500, 200, 50, "Play Again")
        self.game_over = False

    def determine_winner(self):
        # Check for tie
        if self.user_choice == self.computer_choice:
            return "It's a tie!"
        
        # Define winning combinations
        winning_combinations = {
            'scissors': 'paper',
            'paper': 'rock',
            'rock': 'scissors'
        }
        
        # Determine winner based on choices
        if winning_combinations[self.user_choice] == self.computer_choice:
            return "You win!"
        return "Computer wins!"

    def draw(self, surface):
        # Clear screen
        surface.fill(WHITE)
        
        # Draw game title
        title = self.font.render("Rock Paper Scissors", True, BLACK)
        surface.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 50))

        if not self.game_over:
            # Draw choice buttons during gameplay
            for button in self.buttons:
                button.draw(surface)
        else:
            # Draw results screen
            if self.user_choice and self.computer_choice:
                # Show player's choice
                player_text = self.font.render("Your choice:", True, BLACK)
                surface.blit(player_text, (150, 150))
                surface.blit(self.images[self.user_choice], (150, 200))

                # Show computer's choice
                computer_text = self.font.render("Computer's choice:", True, BLACK)
                surface.blit(computer_text, (500, 150))
                surface.blit(self.images[self.computer_choice], (500, 200))

                # Show game result
                result_text = self.font.render(self.result, True, BLACK)
                surface.blit(result_text, (WINDOW_WIDTH//2 - result_text.get_width()//2, 350))

                # Show play again button
                self.play_again_button.draw(surface)

    def handle_event(self, event):
        if not self.game_over:
            # Handle choice selection
            for i, button in enumerate(self.buttons):
                if button.handle_event(event):
                    self.user_choice = self.choices[i]
                    self.computer_choice = random.choice(self.choices)
                    self.result = self.determine_winner()
                    self.game_over = True
        else:
            # Handle play again button
            if self.play_again_button.handle_event(event):
                self.reset_game()

    def reset_game(self):
        # Reset game state for new round
        self.user_choice = None
        self.computer_choice = None
        self.result = None
        self.game_over = False

# Main game loop
def main():
    game = Game()
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        # Update display
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    # Clean up and exit
    pygame.quit()
    sys.exit()

# Start game if script is run directly
if __name__ == "__main__":
    main()
