# Jubran Khoury

import pygame
import sys
import math
import random

# Initialize the game
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Character settings
CHAR_WIDTH = 50
CHAR_HEIGHT = 50
char_speed = 5

# Fireball settings
fireballs = []
FIREBALL_WIDTH = 10
FIREBALL_HEIGHT = 10
fireball_speed = 10
fireball_limit = 10

# Enemy settings
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
enemy_speed = 1  # Slowed down the enemies

# Enemy fireball settings
enemy_fireballs = []
ENEMY_FIREBALL_WIDTH = 10
ENEMY_FIREBALL_HEIGHT = 10
enemy_fireball_speed = 5
enemy_shoot_frequency = 0.02  # Adjust as needed

# Wall settings
walls = []

# Font settings
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)

# Load images with error handling
def load_image(file_name):
    try:
        image = pygame.image.load(file_name)
        return image
    except pygame.error as e:
        print(f"Cannot load image: {file_name}")
        raise SystemExit(e)

background_img = load_image('R.jpeg')
player_img = load_image('solider.png')
enemy_img = load_image('theif-icon.jpg')
fireball_img = load_image('fireball.jpg')
enemy_fireball_img = load_image('fireball.jpg')
wall_img = load_image('wall.jpeg')
cursor_img = load_image('cursor.jpg')  # Load the cursor image

# Resize images
player_img = pygame.transform.scale(player_img, (CHAR_WIDTH, CHAR_HEIGHT))
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
fireball_img = pygame.transform.scale(fireball_img, (FIREBALL_WIDTH, FIREBALL_HEIGHT))
enemy_fireball_img = pygame.transform.scale(enemy_fireball_img, (ENEMY_FIREBALL_WIDTH, ENEMY_FIREBALL_HEIGHT))
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
cursor_img = pygame.transform.scale(cursor_img, (20, 20))  # Resize cursor image

# Define global variables
char_x = SCREEN_WIDTH // 2
char_y = SCREEN_HEIGHT // 2
char_health = 100
enemies = []

def reset_game():
    global char_x, char_y, char_health, fireballs, enemies, enemy_fireballs, walls
    char_x = SCREEN_WIDTH // 2
    char_y = SCREEN_HEIGHT // 2
    char_health = 100
    fireballs = []
    enemy_fireballs = []
    enemies.clear()
    for _ in range(3):  # Number of enemies
        enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        enemy_y = random.randint(0, SCREEN_HEIGHT - ENEMY_HEIGHT)
        enemy_health = 50
        enemies.append([enemy_x, enemy_y, enemy_health])
    walls = [
        (50, 50, 100, 10),  # Top-left corner horizontal
        (50, 50, 10, 100),  # Top-left corner vertical
        (650, 50, 100, 10),  # Top-right corner horizontal
        (740, 50, 10, 100),  # Top-right corner vertical
        (50, 500, 100, 10),  # Bottom-left corner horizontal
        (50, 400, 10, 100),  # Bottom-left corner vertical
        (650, 500, 100, 10),  # Bottom-right corner horizontal
        (740, 400, 10, 100)  # Bottom-right corner vertical
    ]

reset_game()

# Hide the default cursor
pygame.mouse.set_visible(False)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Function to calculate the direction and velocity of the fireball
def calculate_fireball_velocity(start_x, start_y, target_x, target_y, speed):
    angle = math.atan2(target_y - start_y, target_x - start_x)
    velocity_x = speed * math.cos(angle)
    velocity_y = speed * math.sin(angle)
    return velocity_x, velocity_y

# Function to display a message
def display_message(text, color, y_offset=0):
    message = font.render(text, True, color)
    screen.blit(message, [SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2 - message.get_height() // 2 + y_offset])

# Function to draw walls
def draw_walls():
    for wall in walls:
        wall_rect = pygame.Rect(wall)
        screen.blit(pygame.transform.scale(wall_img, (wall[2], wall[3])), wall_rect)

# Function to draw buttons
def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect)
    button_text = small_font.render(text, True, BLACK)
    screen.blit(button_text, (rect.x + (rect.width - button_text.get_width()) // 2, rect.y + (rect.height - button_text.get_height()) // 2))

# Main game loop
running = True
game_over = False
win = False
play_again_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
exit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50)

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                if play_again_rect.collidepoint(event.pos):
                    reset_game()
                    game_over = False
                elif exit_rect.collidepoint(event.pos):
                    running = False
            elif event.button == 1:  # Left mouse button
                if len(fireballs) < fireball_limit:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    fireball_velocity_x, fireball_velocity_y = calculate_fireball_velocity(char_x + CHAR_WIDTH // 2, char_y + CHAR_HEIGHT // 2, mouse_x, mouse_y, fireball_speed)
                    fireballs.append([char_x + CHAR_WIDTH // 2, char_y + CHAR_HEIGHT // 2, fireball_velocity_x, fireball_velocity_y])

    if not game_over:
        # Handle character movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            char_y -= char_speed
        if keys[pygame.K_s]:
            char_y += char_speed
        if keys[pygame.K_a]:
            char_x -= char_speed
        if keys[pygame.K_d]:
            char_x += char_speed

        # Update fireball positions
        for fireball in fireballs:
            fireball[0] += fireball[2]
            fireball[1] += fireball[3]

        # Remove fireballs that go off-screen
        fireballs = [fireball for fireball in fireballs if 0 <= fireball[0] <= SCREEN_WIDTH and 0 <= fireball[1] <= SCREEN_HEIGHT]

        # Update enemy positions and fireballs
        for enemy in enemies:
            # Move the enemy towards the player
            if enemy[0] < char_x:
                enemy[0] += enemy_speed
            if enemy[0] > char_x:
                enemy[0] -= enemy_speed
            if enemy[1] < char_y:
                enemy[1] += enemy_speed
            if enemy[1] > char_y:
                enemy[1] -= enemy_speed

            # Enemy shoots at the player
            if random.random() < enemy_shoot_frequency:  # Adjust the shooting frequency
                enemy_fireball_velocity_x, enemy_fireball_velocity_y = calculate_fireball_velocity(enemy[0] + ENEMY_WIDTH // 2, enemy[1] + ENEMY_HEIGHT // 2, char_x, char_y, enemy_fireball_speed)
                enemy_fireballs.append([enemy[0] + ENEMY_WIDTH // 2, enemy[1] + ENEMY_HEIGHT // 2, enemy_fireball_velocity_x, enemy_fireball_velocity_y])

        # Update enemy fireball positions
        for enemy_fireball in enemy_fireballs:
            enemy_fireball[0] += enemy_fireball[2]
            enemy_fireball[1] += enemy_fireball[3]

        # Remove enemy fireballs that go off-screen
        enemy_fireballs = [enemy_fireball for enemy_fireball in enemy_fireballs if 0 <= enemy_fireball[0] <= SCREEN_WIDTH and 0 <= enemy_fireball[1] <= SCREEN_HEIGHT]

        # Clear the screen and draw the background
        screen.blit(background_img, (0, 0))

        # Draw walls
        draw_walls()

        # Draw the character
        screen.blit(player_img, (char_x, char_y))

        # Draw fireballs
        for fireball in fireballs:
            screen.blit(fireball_img, (fireball[0], fireball[1]))

        # Draw enemies
        for enemy in enemies:
            screen.blit(enemy_img, (enemy[0], enemy[1]))

        # Draw enemy fireballs
        for enemy_fireball in enemy_fireballs:
            screen.blit(enemy_fireball_img, (enemy_fireball[0], enemy_fireball[1]))

        # Check for collisions between fireballs and enemies
        for fireball in fireballs[:]:
            for enemy in enemies[:]:
                if enemy[0] < fireball[0] < enemy[0] + ENEMY_WIDTH and enemy[1] < fireball[1] < enemy[1] + ENEMY_HEIGHT:
                    fireballs.remove(fireball)
                    enemy[2] -= 10  # Reduce enemy health by 10
                    if enemy[2] <= 0:
                        enemies.remove(enemy)
                    break

        # Check for collisions between enemy fireballs and the player
        for enemy_fireball in enemy_fireballs[:]:
            if char_x < enemy_fireball[0] < char_x + CHAR_WIDTH and char_y < enemy_fireball[1] < char_y + CHAR_HEIGHT:
                enemy_fireballs.remove(enemy_fireball)
                char_health -= 10  # Reduce player health by 10
                if char_health <= 0:
                    game_over = True
                    win = False  # Player lost

        # Check for collisions between enemy fireballs and walls
        for enemy_fireball in enemy_fireballs[:]:
            for wall in walls:
                wall_rect = pygame.Rect(wall)
                if wall_rect.collidepoint(enemy_fireball[0], enemy_fireball[1]):
                    enemy_fireballs.remove(enemy_fireball)
                    break

        # Player health
        health_text = small_font.render(f'Health: {char_health}%', True, BLACK)
        screen.blit(health_text, (10, 10))

        # Check if all enemies are defeated
        if not enemies:
            game_over = True
            win = True  # Player won

    else:
        if win:
            display_message('You Win!', GREEN, y_offset=-50)
        else:
            display_message('You Lost!', RED, y_offset=-50)
        draw_button('Play Again', play_again_rect, GRAY)
        draw_button('Exit', exit_rect, GRAY)

    # Cursor
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(cursor_img, (mouse_x - 10, mouse_y - 10))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
