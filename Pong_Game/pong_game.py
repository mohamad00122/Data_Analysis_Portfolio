import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and game variables
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90
player_score, computer_score = 0, 0
game_over = False
game_paused = False
player_vs_player = False

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5

    def move(self, up=True):
        if up:
            self.y = max(self.y - self.speed, 0)
        else:
            self.y = min(self.y + self.speed, SCREEN_HEIGHT - PADDLE_HEIGHT)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Ball class
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_speed = 3 * random.choice([-1, 1])
        self.y_speed = 3 * random.choice([-1, 1])

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), BALL_RADIUS)

    def bounce(self, paddles):
        if self.y - BALL_RADIUS <= 0 or self.y + BALL_RADIUS >= SCREEN_HEIGHT:
            self.y_speed *= -1

        for paddle in paddles:
            if self.x - BALL_RADIUS <= paddle.x + PADDLE_WIDTH and \
               self.x + BALL_RADIUS >= paddle.x and \
               self.y + BALL_RADIUS >= paddle.y and \
               self.y - BALL_RADIUS <= paddle.y + PADDLE_HEIGHT:
                self.x_speed *= -1
                break

def draw_middle_line(screen):
    for i in range(0, SCREEN_HEIGHT, 20):
        if i % 40 == 0:
            pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, i), (SCREEN_WIDTH // 2, i + 10))

def draw_score(screen, player_score, computer_score):
    font = pygame.font.SysFont(None, 74)
    text = font.render(str(player_score), True, WHITE)
    screen.blit(text, (250, 10))
    text = font.render(str(computer_score), True, WHITE)
    screen.blit(text, (SCREEN_WIDTH - 250, 10))

def draw_menu(screen):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 74)
    title_text = font.render("Pong Game", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 150))

    pvp_text = font.render("Player vs Player", True, WHITE)
    pvp_rect = pvp_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(pvp_text, pvp_rect.topleft)

    pvc_text = font.render("Player vs Computer", True, WHITE)
    pvc_rect = pvc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(pvc_text, pvc_rect.topleft)

    pygame.display.flip()
    return pvp_rect, pvc_rect

def draw_pause_menu(screen):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 74)
    pause_text = font.render("Paused", True, WHITE)
    screen.blit(pause_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
    resume_text = font.render("Resume", True, WHITE)
    screen.blit(resume_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
    quit_text = font.render("Quit", True, WHITE)
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 60))
    pygame.display.flip()

def computer_ai(ball, computer_paddle):
    if not player_vs_player:
        if computer_paddle.y + PADDLE_HEIGHT // 2 < ball.y:
            computer_paddle.move(up=False)
        elif computer_paddle.y + PADDLE_HEIGHT // 2 > ball.y:
            computer_paddle.move(up=True)

# Create game objects
player_paddle = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
computer_paddle = Paddle(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Main game loop
clock = pygame.time.Clock()
show_menu = True
while not game_over:
    if show_menu:
        pvp_rect, pvc_rect = draw_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                show_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if pvp_rect.collidepoint(mouse_x, mouse_y):
                    player_vs_player = True
                    show_menu = False
                if pvc_rect.collidepoint(mouse_x, mouse_y):
                    player_vs_player = False
                    show_menu = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = not game_paused

        if game_paused:
            draw_pause_menu(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if SCREEN_WIDTH // 2 - 100 < mouse_x < SCREEN_WIDTH // 2 + 100:
                        if SCREEN_HEIGHT // 2 - 20 < mouse_y < SCREEN_HEIGHT // 2 + 20:
                            game_paused = False
                        elif SCREEN_HEIGHT // 2 + 60 < mouse_y < SCREEN_HEIGHT // 2 + 100:
                            game_over = True
        else:
            keys = pygame.key.get_pressed()
            # Player 1 controls (left side)
            if player_vs_player:
                if keys[pygame.K_w]:
                    player_paddle.move(up=True)
                if keys[pygame.K_s]:
                    player_paddle.move(up=False)
            else:
                if keys[pygame.K_UP]:
                    player_paddle.move(up=True)
                if keys[pygame.K_DOWN]:
                    player_paddle.move(up=False)

            # Player 2 or Computer controls
            if player_vs_player:
                if keys[pygame.K_UP]:
                    computer_paddle.move(up=True)
                if keys[pygame.K_DOWN]:
                    computer_paddle.move(up=False)
            else:
                computer_ai(ball, computer_paddle)

            ball.move()
            ball.bounce([player_paddle, computer_paddle])

            if ball.x < 0:
                computer_score += 1
                ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            elif ball.x > SCREEN_WIDTH:
                player_score += 1
                ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

            screen.fill(BLACK)
            player_paddle.draw(screen)
            computer_paddle.draw(screen)
            ball.draw(screen)
            draw_middle_line(screen)
            draw_score(screen, player_score, computer_score)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
