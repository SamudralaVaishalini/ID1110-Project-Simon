import pygame
import random

# COLORS (r, g, b)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
PINK=(172, 39, 108)
DARKPINK=(245, 2, 128)
YELLOW=(249, 248, 113)
DARKYELLOW=(250, 248, 10)
GREEN=(14, 230, 168)
DARKGREEN=(25, 245, 10)
VIOLET=(143, 117, 206)
DARKVIOLET=(83, 33, 204)

# game settings
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Simon"
BUTTON_SIZE = 200
ANIMATION_SPEED = 20

# Load background image
BGCOLOR = pygame.image.load('ocean.jpg')

class Button:
    # Initialize the Button object
    def __init__(self, x, y, colour):
        self.x, self.y = x, y  # Set the position of the button
        self.colour = colour    # Set the color of the button

    # Draw the button on the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, BUTTON_SIZE, BUTTON_SIZE))

    # Check if the button is clicked
    def clicked(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + BUTTON_SIZE and self.y <= mouse_y <= self.y + BUTTON_SIZE

# Define the UIElement class
class UIElement:
    # Initialize the UIElement object
    def __init__(self, x, y, text):
        self.x, self.y = x, y  # Set the position of the UI element
        self.text = text        # Set the text content of the UI element

    # Draw the UI element on the screen
    def draw(self, screen):
        font = pygame.font.Font("moto-verse.ttf", 16)  # Load a font for rendering text
        text = font.render(self.text, True, BLACK)     # Render the text with the font and color
        screen.blit(text, (self.x, self.y))            # Blit the text onto the screen at the specified position
class Game:
    # Initialize the game
    def __init__(self):
        pygame.init()  # Initialize pygame
        # Set window dimensions
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # Load game icon
        icon = pygame.image.load("simon.png")
        # Set game icon
        pygame.display.set_icon(icon)
        # Set game title
        pygame.display.set_caption(TITLE)
        # Create a clock object to control frame rate
        self.clock = pygame.time.Clock()

        # Define color schemes for button animations
        self.flash_colours = [PINK, YELLOW, GREEN, VIOLET]
        self.colours = [DARKPINK, DARKYELLOW, DARKGREEN, DARKVIOLET]

        # Define positions and colors for the buttons
        self.buttons = [
            Button(165, 90, DARKPINK),
            Button(385, 90, DARKYELLOW),
            Button(165, 310, DARKGREEN),
            Button(385, 310, DARKVIOLET),
        ]

    # Get the high score from a file
    def get_high_score(self):
        with open("high_score.txt", "r") as file:
            # Read the high score
            score = file.read()
        # Return the high score as an integer
        return int(score)

    # Save the high score to a file
    def save_score(self):
        with open("high_score.txt", "w") as file:
            if self.score > self.high_score:
                # If current score is higher than high score, write current score to file
                file.write(str(self.score))

            else:
                # Otherwise, write high score to file
                file.write(str(self.high_score))
                
    # Reset game variables for a new game
    def new(self):
        # Initialize game variables
        self.waiting_input = False
        self.pattern = []
        self.current_step = 0
        self.score = 0
        # Get the high score
        self.high_score = self.get_high_score()
      # Display "Game Over" text on the screen
    def game_over_text(self):
        # Load font for "Game Over" text
        over_font = pygame.font.Font('INFECTED.ttf', 150)
        # Render "Game Over" text
        over_text = over_font.render('GAME OVER', True, (0, 0, 0))
        # Draw "Game Over" text on the screen
        self.screen.blit(over_text, (80, 200))

    # Run the game loop
    def run(self):
        # Set playing flag to True
        self.playing = True
        # Main game loop
        while self.playing:
            # Control frame rate
            self.clock.tick(FPS)
            # Reset clicked button
            self.clicked_button = None
            # Handle events
            self.events()
            # Draw game elements
            self.draw()
            # Update game state
            self.update()

    # Update game state
    def update(self):
        # If waiting for input
        if not self.waiting_input:
            # Wait for a short duration
            pygame.time.wait(1000)
            # Add a new color to the pattern and display it
            self.pattern.append(random.choice(self.colours))

            for button in self.pattern:
                self.button_animation(button)
                pygame.time.wait(200)
            # Now waiting for player input
            self.waiting_input = True
        else:
            # Check if player input matches the pattern
            if self.clicked_button and self.clicked_button == self.pattern[self.current_step]:
                # If correct button clicked, move to the next step
                self.button_animation(self.clicked_button)
                self.current_step += 1
                # If pattern completed, increase score and reset variables
                if self.current_step == len(self.pattern):
                    self.score += 1
                    self.waiting_input = False
                    self.current_step = 0

            # If wrong button clicked, end the game
            elif self.clicked_button and self.clicked_button != self.pattern[self.current_step]:
                self.game_over_text()
                self.game_over_animation()
                self.save_score()
                self.playing = False

    # Animate the button flash
    def button_animation(self, colour):
        # Loop through the colors and buttons to find the matching color
        for i in range(len(self.colours)):
            if self.colours[i] == colour:
                # Assign the flash color and corresponding button
                flash_colour = self.flash_colours[i]
                button = self.buttons[i]

        # Copy the original screen to avoid modifying it directly
        original_surface = self.screen.copy()
        # Create a surface for the flash effect with transparency
        flash_surface = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE))
        flash_surface = flash_surface.convert_alpha()
        r, g, b = flash_colour  # Get the RGB components of the flash color

        # Loop through the animation steps for increasing and decreasing alpha
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # Loop through alpha values within the range with the given step
            for alpha in range(start, end, ANIMATION_SPEED * step):
                # Copy the original screen to reset it for the next frame
                self.screen.blit(original_surface, (0, 0))
                # Fill the flash surface with the flash color and current alpha
                flash_surface.fill((r, g, b, alpha))
                # Blit the flash surface onto the screen at the button's position
                self.screen.blit(flash_surface, (button.x, button.y))
                # Update the display to show the changes
                pygame.display.update()
                # Control the frame rate
                self.clock.tick(FPS)
        # After the animation is complete, restore the original screen
        self.screen.blit(original_surface, (0, 0))
     # Animate the screen flash when game over
    def game_over_animation(self):
        # Copy the original screen to avoid modifying it directly
        original_surface = self.screen.copy()
        # Create a surface for the flash effect with transparency
        flash_surface = pygame.Surface((self.screen.get_size()))
        flash_surface = flash_surface.convert_alpha()

        r, g, b = WHITE
        # Loop through the animation steps for flashing effect
        for _ in range(3):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                # Loop through alpha values within the range with the given step
                for alpha in range(start, end, ANIMATION_SPEED * step):
                    # Copy the original screen to reset it for the next frame
                    self.screen.blit(original_surface, (0, 0))
                    # Fill the flash surface with white color and current alpha
                    flash_surface.fill((r, g, b, alpha))
                    # Blit the flash surface onto the screen
                    self.screen.blit(flash_surface, (0, 0))
                    # Update the display to show the changes
                    pygame.display.update()
                    # Control the frame rate
                    self.clock.tick(FPS)

    # Draw elements on the screen
    def draw(self):
        # Fill the screen with white color
        self.screen.fill((255, 255, 255))
        # Draw background image
        self.screen.blit(BGCOLOR, (0, 0))
        # Draw score and high score text on the screen
        UIElement(170, 20, f"Score: {str(self.score)}").draw(self.screen)
        UIElement(370, 20, f"High score: {str(self.high_score)}").draw(self.screen)
        # Draw buttons on the screen
        for button in self.buttons:
            button.draw(self.screen)
        # Update the display
        pygame.display.update()

