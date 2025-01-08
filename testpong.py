import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
FPS = 60
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_SIZE = 20

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Game variables
ball_speed = [6, 6]
paddle_speed = 8
score_limit = 10
game_mode = None  # 'single' or 'two'
menu_active = True


def draw_text(text, font, color, surface, x, y):
    """Helper function to draw text."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def create_button(x, y, width, height, text, font, color, text_color):
    """Helper function to create a button."""
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect)
    draw_text(text, font, text_color, screen, x + width // 2, y + height // 2)
    return rect


def menu():
    """Main menu screen with clickable buttons."""
    global menu_active, game_mode
    while menu_active:
        screen.fill(BLUE)

        # Create buttons
        single_player_button = create_button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50, "Single Player", font, RED, WHITE)
        two_player_button = create_button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Two Player", font, RED, WHITE)
        exit_button = create_button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Exit", font, RED, WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_player_button.collidepoint(event.pos):
                    game_mode = 'single'
                    score_menu()
                if two_player_button.collidepoint(event.pos):
                    game_mode = 'two'
                    score_menu()
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit


def score_menu():
    """Score limit selection menu."""
    global menu_active, score_limit
    while menu_active:
        screen.fill(BLUE)

        # Create buttons
        score_10_button = create_button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50, "10 Points", font, RED, WHITE)
        score_20_button = create_button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50, "20 Points", font, RED, WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if score_10_button.collidepoint(event.pos):
                    score_limit = 10
                    menu_active = False
                if score_20_button.collidepoint(event.pos):
                    score_limit = 20
                    menu_active = False


def game_loop():
    """Main game loop."""
    global menu_active

    # Initialize game objects
    ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
    player1 = pygame.Rect(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    player2 = pygame.Rect(SCREEN_WIDTH - 40, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    player1_score = 0
    player2_score = 0
    ball_dx, ball_dy = ball_speed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_active = True
                    menu()

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Player 1 movement
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= paddle_speed
        if keys[pygame.K_s] and player1.bottom < SCREEN_HEIGHT:
            player1.y += paddle_speed

        # Player 2 movement
        if game_mode == 'two':
            if keys[pygame.K_UP] and player2.top > 0:
                player2.y -= paddle_speed
            if keys[pygame.K_DOWN] and player2.bottom < SCREEN_HEIGHT:
                player2.y += paddle_speed
        elif game_mode == 'single':
            # Simple AI for single-player mode
            if ball.centery > player2.centery and player2.bottom < SCREEN_HEIGHT:
                player2.y += paddle_speed
            if ball.centery < player2.centery and player2.top > 0:
                player2.y -= paddle_speed

        # Move the ball
        ball.x += ball_dx
        ball.y += ball_dy

        # Ball collision with top and bottom walls
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_dy = -ball_dy

        # Ball collision with paddles
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_dx = -ball_dx

        # Ball out of bounds
        if ball.left <= 0:
            player2_score += 1
            ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
            ball_dx = -ball_dx
        if ball.right >= SCREEN_WIDTH:
            player1_score += 1
            ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
            ball_dx = -ball_dx

        # Check score limit
        if player1_score >= score_limit or player2_score >= score_limit:
            winner = "Player 1" if player1_score > player2_score else "Player 2"
            if game_mode == 'single' and player2_score > player1_score:
                winner = "AI"
            draw_text(f"{winner} Wins!", large_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(3000)
            menu()

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player1)
        pygame.draw.rect(screen, WHITE, player2)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        # Draw scores
        draw_text(str(player1_score), font, WHITE, screen, SCREEN_WIDTH // 4, 20)
        draw_text(str(player2_score), font, WHITE, screen, SCREEN_WIDTH * 3 // 4, 20)

        pygame.display.flip()
        clock.tick(FPS)


# Start the game
menu()
game_loop()