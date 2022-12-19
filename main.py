import random
import pygame
from pygame.locals import *

# Initialize Pygame and set screen dimensions
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title and icon
pygame.display.set_caption("Physics Simulation")

# Create a ball with a random position and speed
class Ball:
    """Moving ball"""

    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed_x = random.randint(-10, 10)
        self.speed_y = random.randint(-10, 10)
        self.radius = 10
        self.prev_speed_y = self.speed_y
        self.g = 9.82
        self.t_scale = 0.5
        self.change_value = 'g'

    # Update the ball's position based on its speed and time scale
    def move(self):
        self.speed_y += self.g * self.t_scale
        self.x += self.speed_x * self.t_scale
        self.y += self.speed_y * self.t_scale

        # Check if the screen is being clicked and update the balls position
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.x = mouse_x
            self.y = mouse_y
            self.speed_x, self.speed_y = pygame.mouse.get_rel()

        # Check for a collision with the ground and bounce off. Reduces speed on the X-axis by 5% if touching the ground
        if self.y > SCREEN_HEIGHT - self.radius:
            self.y = SCREEN_HEIGHT - self.radius
            self.speed_y *= -0.85
            self.speed_x *= 0.95

        # Check for a collision with the walls and bounce off
        if self.x > SCREEN_WIDTH - self.radius or self.x < self.radius:
            self.speed_x *= -1

    # Function to change the values
    def set_values(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_g]:
            self.change_value = 'g'

        elif key[pygame.K_t]:
            self.change_value = 't'

        # Change gravity
        if self.change_value == 'g':
            if key[K_UP] and self.g <= 100:
                self.g += 0.5

            elif key[K_DOWN] and self.g >= 0:
                self.g -= 0.5

        # Max and min limits for gravity
        if self.g <= 0:
            self.g = 0

        elif self.g >= 100:
            self.g = 100

        # Change the time scale
        if self.change_value == 't':
            if key[K_UP] and self.g <= 100:
                self.t_scale += 0.05

            elif key[K_DOWN] and self.g >= 0:
                self.t_scale -= 0.05

        # Max and min limits for the time scale
        if self.t_scale <= 0:
            self.t_scale = 0

        elif self.t_scale >= 2:
            self.t_scale = 2

        # Reset values
        if key[K_SPACE]:
            self.g = 9.82
            self.t_scale = 0.5

    # Draw the ball on the screen
    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255),
                           (self.x, self.y), self.radius)
        font = pygame.font.SysFont(None, 24)

        # Change color of text based on which value you're changing
        if self.change_value == 'g':
            screen.blit(font.render(
                f'Gravity: {self.g:.2f} m/s (g)', True, (0, 255, 0)), (20, 15))
            screen.blit(font.render(
                f'Time Scale: {self.t_scale:.2f} (t)', True, (255, 255, 255)), (20, 45))

        elif self.change_value == 't':
            screen.blit(font.render(
                f'Gravity: {self.g:.2f} m/s (g)', True, (255, 255, 255)), (20, 20))
            screen.blit(font.render(
                f'Time Scale: {self.t_scale:.2f} (t)', True, (0, 255, 0)), (20, 45))

        # Display speed
        screen.blit(font.render(
            f'Speed Y-axis: {self.speed_y:.2f} m/s', True, (255, 255, 255)), (20, 75))
        screen.blit(font.render(
            f'Speed X-axis: {self.speed_x:.2f} m/s', True, (255, 255, 255)), (20, 105))

    # Single function you can call to easily call all other functions
    def update(self):
        self.move()
        self.set_values()
        self.draw()


# Create a list of balls
ball = Ball()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.time.Clock().tick(60)

    screen.fill((0, 0, 0))
    # Update the screen and draw the ball
    ball.update()
    pygame.display.flip()
