import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
BALL_SIZE = 30  # Diameter of each ball
GRID_ROWS = 9
GRID_COLS = 7
GRID_WIDTH = 192  # Width of the 9x7 grid
GRID_HEIGHT = 240  # Height of the 9x7 grid

# Larger window size (wider than tall)
window_width = 600  # Window width will be twice the grid width
window_height = 450  # Window height will be 1.5 times the grid height

# Create the Pygame window
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Billiard Ball Simulation SWITCH")

# Colors
black = (30, 50, 30)
white = (255, 255, 255)  # Define the color white
red = (255, 100, 100)
blue = (100, 100, 255)
green = (100, 255, 100)
gray = (169, 169, 169)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Ball class
class Ball:
    def __init__(self, x, y, radius, color, dx, dy):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dx = dx
        self.dy = dy
        self.active = True  # Ball is active by default
        self.save_x = 0
        self.save_y = 0

    def move(self):
        if self.active:
            # Update ball position
            self.x += self.dx
            self.y += self.dy

            # Check for collisions with the points
            point1 = (120, 48)
            point2 = (48, 168)

            if self.check_point_collision(point1):
                self.turn_90_degrees()
            
            if self.check_point_collision(point2):
                self.turn_90_degrees()

            # Ensure balls stay within the 9x7 box
            if self.x - self.radius < -10 or self.x + self.radius >= GRID_WIDTH + 10:
                self.save_x = -self.dx
                self.save_y = -self.dy
                self.dy = -self.dy
                self.dx = -self.dx
                return 0
            if self.y - self.radius < -10 or self.y + self.radius >= GRID_HEIGHT + 10:
                self.save_x = -self.dx
                self.save_y = -self.dy
                self.dy = -self.dy
                self.dx = -self.dx
                return 0

        return 1

    def check_point_collision(self, point):
        # calculate the distance between the ball and the point
        dx = self.x - point[0]
        dy = self.y - point[1]
        distance = math.hypot(dx, dy)

        # check if the ball's radius hits the point/mirror
        return distance <= self.radius + 2

    def draw(self, screen, offset_x, offset_y):
        if self.active:
            # Draw the ball with offset to center the grid
            pygame.draw.circle(screen, self.color, (int(self.x) + offset_x, int(self.y) + offset_y), self.radius)

    def check_collision(self, other_ball):
        # check if this ball collides with another ball
        dx = self.x - other_ball.x
        dy = self.y - other_ball.y
        distance = math.hypot(dx, dy)
        return distance < self.radius + other_ball.radius

    def turn_90_degrees(self):
        # Swap dx and dy to simulate a 90-degree turn
        self.dx, self.dy = self.dy, self.dx

# Initialize balls
balls = [
    Ball(12, 84, BALL_SIZE // 2, blue, 1, 0),
    Ball(84, 12, BALL_SIZE // 2, red, 0, 1)
]

# Calculate the position to center the grid in the window
grid_x_offset = (window_width - GRID_WIDTH) // 2
grid_y_offset = (window_height - GRID_HEIGHT) // 2 - 40

# Button class to create and handle button actions
class Button:
    def __init__(self, text, x, y, width, height, color, text_color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 24)  # Smaller font size
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

# Function to reverse the direction of the balls
# def reverse_direction():
#     for ball in balls:
#         ball.dx = ball.save_x
#         ball.dy = ball.save_y

# Start button, toggle ball buttons, reset button
button_width = 100
button_height = 50
button_spacing = 20  # Space between buttons
total_buttons_width = 4 * button_width + 3 * button_spacing  # Total width of all buttons and spacing
buttons_start_x = (window_width - total_buttons_width) // 2   # Center buttons

start_button = Button("Start/Reverse", buttons_start_x-20, window_height - 70, button_width+20, button_height, green, black)
ball1_button = Button("x", buttons_start_x + button_width + button_spacing, window_height - 70, button_width, button_height, blue, black)
ball2_button = Button("c", buttons_start_x + 2 * (button_width + button_spacing), window_height - 70, button_width, button_height, red, black)
reset_button = Button("Reset", buttons_start_x + 3 * (button_width + button_spacing), window_height - 70, button_width, button_height, gray, black)

# Start/Stop state
simulation_running = False

# Diagonal bars coordinates
bar1 = [(108, 36), (132, 60)]
bar2 = [(36, 156), (60, 180)]

# Initial positions for resetting
initial_positions = [(12, 84), (84, 12)]

# event queue loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if start_button.is_hovered(pos):
                simulation_running = not simulation_running  
            if ball1_button.is_hovered(pos):
                balls[0].active = not balls[0].active  
            if ball2_button.is_hovered(pos):
                balls[1].active = not balls[1].active 
            if reset_button.is_hovered(pos):
                # reset balls to initial state
                for i, ball in enumerate(balls):
                    simulation_running = 0
                    ball.x, ball.y = initial_positions[i]
                    ball.dx, ball.dy = (1, 0) if i == 0 else (0, 1)
                    ball.active = True

    # move balls if simulation is running
    stop = 0
    if simulation_running:
        stop = 1
        for ball in balls:
            if not ball.move(): stop = 0

        # Check for collisions between balls and turn them 90 degrees if they collide
        if balls[0].check_collision(balls[1]):
            balls[0].turn_90_degrees()
            balls[1].turn_90_degrees()

    simulation_running = stop

    # Draw everything
    screen.fill(black)  # Background

    # Draw the balls
    for ball in balls:
        ball.draw(screen, grid_x_offset, grid_y_offset)

    # Draw the grid boundary (9x7 box) in the center of the window
    pygame.draw.rect(screen, white, (grid_x_offset, grid_y_offset, GRID_WIDTH, GRID_HEIGHT), 3)

    # Draw the bars
    pygame.draw.line(screen, white, (grid_x_offset + bar1[0][0], grid_y_offset + bar1[0][1]),
                     (grid_x_offset + bar1[1][0], grid_y_offset + bar1[1][1]), 5)
    pygame.draw.line(screen, white, (grid_x_offset + bar2[0][0], grid_y_offset + bar2[0][1]),
                     (grid_x_offset + bar2[1][0], grid_y_offset + bar2[1][1]), 5)

    # Draw buttons
    start_button.draw(screen)
    ball1_button.draw(screen)
    ball2_button.draw(screen)
    reset_button.draw(screen)

    font = pygame.font.Font(None, 30) 
    x_text = "x"
    x_surface = font.render(x_text, True, white)  
    screen.blit(x_surface, (175, 138)) 
    c_text = "c"
    c_surface = font.render(c_text, True, white)  
    screen.blit(c_surface, (282, 35))
    screen.blit(c_surface, (290, 320))
    not_cx_text = "~cx"
    not_cx_surface = font.render(not_cx_text, True, white)  
    screen.blit(not_cx_surface, (410, 138))
    cx_text = "cx"
    cx_surface = font.render(cx_text, True, white)  
    screen.blit(cx_surface, (415, 194))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
