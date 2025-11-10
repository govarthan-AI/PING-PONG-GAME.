import pygame
import sys

# Initialize pygame
pygame.init()

# Window setup
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Ping Pong Game")

# Font and score
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

# Paddle settings
width = 100
height = 10
speed = 5

# Ball settings
radius = 10

clock = pygame.time.Clock()

# Function to reset everything
def reset_game():
    global x, y, ball_x, ball_y, ball_speed_x, ball_speed_y, total, game_active, game_over
    x = 450
    y = 550
    ball_x = 500
    ball_y = 100
    ball_speed_x = 4
    ball_speed_y = 4
    total = 0
    game_active = False
    game_over = False

reset_game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if not game_active and not game_over and event.key == pygame.K_SPACE:
                # Start the game
                game_active = True
            elif game_over and event.key == pygame.K_SPACE:
                # Restart the game
                reset_game()
                game_active = True
            elif game_over and event.key == pygame.K_ESCAPE:
                running = False

    if game_active:
        # Paddle control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed

        # Keep paddle inside screen
        x = max(0, min(x, 1000 - width))

        # Move ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Bounce off walls
        if ball_x - radius <= 0 or ball_x + radius >= 1000:
            ball_speed_x *= -1
        if ball_y - radius <= 0:
            ball_speed_y *= -1

        # Paddle collision
        if (y - radius <= ball_y <= y + height) and (x <= ball_x <= x + width):
            ball_speed_y *= -1
            total += 1

        # Ball goes below paddle → Game Over
        if ball_y + radius >= 600:
            game_over = True
            game_active = False

        # Draw gameplay
        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (0, 0, 0), (ball_x, ball_y), radius)
        pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height))
        text = font.render(f"Score: {total}", True, (0, 0, 0))
        screen.blit(text, (50, 50))

    elif not game_active and not game_over:
        # Start screen
        screen.fill((255, 255, 255))
        msg = font.render("Press SPACE to START", True, (255, 0, 0))
        screen.blit(msg, (300, 280))

    elif game_over:
        # Game Over Screen
        screen.fill((255, 255, 255))
        over_text = font.render("GAME OVER!", True, (255, 0, 0))
        score_text = font.render(f"Final Score: {total}", True, (0, 0, 0))
        restart_text = small_font.render("Press SPACE to RESTART or ESC to QUIT", True, (0, 0, 0))
        screen.blit(over_text, (400, 230))
        screen.blit(score_text, (400, 290))
        screen.blit(restart_text, (300, 350))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()

