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
