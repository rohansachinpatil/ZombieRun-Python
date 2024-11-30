import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set Up Display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Zombie Running Game')

# Load Images
bg_image1 = pygame.image.load(r"C:\P R O G R A M I N G\RUNNING GAME\img\background.png")
bg_image2 = pygame.image.load(r"C:\P R O G R A M I N G\RUNNING GAME\img\background3.jpg")
bg_image3 = pygame.image.load(r"C:\P R O G R A M I N G\RUNNING GAME\img\background4.jpg")
start_button = pygame.image.load(r'C:\P R O G R A M I N G\RUNNING GAME\img\startbutton.png')
obstacle_image = pygame.image.load(r'C:\P R O G R A M I N G\RUNNING GAME\img\obstacle.png')
obstacle2_image = pygame.image.load(r'C:\P R O G R A M I N G\RUNNING GAME\img\obstacle2.png')
obstacle3_image = pygame.image.load(r'C:\P R O G R A M I N G\RUNNING GAME\img\obstacle3.png')
zombie_image = pygame.image.load(r'C:\P R O G R A M I N G\RUNNING GAME\img\zombiepng.png')

# Resize Images
bg_image1 = pygame.transform.scale(bg_image1, (screen_width, screen_height))
bg_image2 = pygame.transform.scale(bg_image2, (screen_width, screen_height))
bg_image3 = pygame.transform.scale(bg_image3, (screen_width, screen_height))
zombie_image = pygame.transform.scale(zombie_image, (200, 200))  # No zoom on zombie
obstacle_image = pygame.transform.scale(obstacle_image, (80, 80))
obstacle2_image = pygame.transform.scale(obstacle2_image, (80, 80))
obstacle3_image = pygame.transform.scale(obstacle3_image, (80, 80))

# Define Game Variables
zombie_width, zombie_height = zombie_image.get_width(), zombie_image.get_height()
zombie_x = 100
zombie_y = screen_height - zombie_height - 100  # Shifted up by 50 pixels
velocity = 10
jump_velocity = 20
gravity = 1
is_jumping = False
jump_count = jump_velocity
score = 0
ground_y = screen_height - 100  # Shifted up by 50 pixels

# Background Variables
bg_images = [bg_image1, bg_image2, bg_image3]
bg_index = 0
bg_x = 0
bg_speed = 10  # Set background speed to match game speed

# File to store highest score
score_file = 'highest_score.txt'

# Load Highest Score
def load_highest_score():
    if os.path.exists(score_file):
        with open(score_file, 'r') as file:
            return int(file.read())
    return 0

# Save Highest Score
def save_highest_score(score):
    with open(score_file, 'w') as file:
        file.write(str(score))

highest_score = load_highest_score()

# Create a list of obstacle images
obstacle_images = [obstacle_image, obstacle2_image, obstacle3_image]

# Game Loop
clock = pygame.time.Clock()
run = True
start_game = False
obstacles = [[screen_width, ground_y - obstacle_image.get_height(), random.choice(obstacle_images)]]
game_speed = bg_speed  # Set game speed to the same as background speed

while run:
    # Scroll Background
    bg_x -= bg_speed
    if bg_x <= -screen_width:
        bg_x = 0
        bg_index = (bg_index + 1) % len(bg_images)
    
    # Draw Background
    screen.blit(bg_images[bg_index], (bg_x, 0))
    screen.blit(bg_images[(bg_index + 1) % len(bg_images)], (bg_x + screen_width, 0))
    
    if not start_game:
        start_button_rect = start_button.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(start_button, start_button_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(x, y):
                    start_game = True
                    score = 0
                    obstacles = [[screen_width, ground_y - obstacle_image.get_height(), random.choice(obstacle_images)]]
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    is_jumping = True
                    jump_count = jump_velocity

        # Update Zombie Position
        if is_jumping:
            zombie_y -= jump_count
            jump_count -= gravity
            if jump_count < -jump_velocity:
                is_jumping = False
        else:
            if zombie_y < ground_y - zombie_height:
                zombie_y += gravity * 2
            else:
                zombie_y = ground_y - zombie_height

        # Draw Zombie
        screen.blit(zombie_image, (zombie_x, zombie_y))

        # Draw Obstacles
        for obstacle in obstacles:
            obstacle[0] -= game_speed
            if obstacle[0] < -obstacle_image.get_width():
                obstacles.remove(obstacle)
                # Add a new obstacle with a random type
                obstacles.append([screen_width + random.randint(300, 500), ground_y - obstacle_image.get_height(), random.choice(obstacle_images)])
            screen.blit(obstacle[2], (obstacle[0], obstacle[1]))

        # Check Collision
        for obstacle in obstacles:
            if zombie_x + zombie_width > obstacle[0] and zombie_x < obstacle[0] + obstacle[2].get_width():
                if zombie_y + zombie_height > obstacle[1]:
                    start_game = False
                    if score > highest_score:
                        highest_score = score
                        save_highest_score(highest_score)
                    score = 0

        # Increase game speed to increase difficulty
        if score % 100 == 0 and game_speed < 20:
            game_speed += 1
            bg_speed = game_speed  # Synchronize background speed with game speed

        score += 1
        font = pygame.font.SysFont('arial', 30)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        highest_score_text = font.render(f'Highest Score: {highest_score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(highest_score_text, (10, 50))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
