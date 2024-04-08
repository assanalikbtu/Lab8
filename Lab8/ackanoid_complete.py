import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1200, 800
FRAMES_PER_SECOND = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
done = False
background_color = (0, 0, 0)


class Paddle:
    def __init__(self, width, height, velocity):
        self.width = width
        self.height = height
        self.velocity = velocity
        self.rect = pygame.Rect(WIDTH // 2 - self.width // 2, HEIGHT - self.height - 30, self.width, self.height)

    def move_left(self):
        if self.rect.left > 0:
            self.rect.left -= self.velocity

    def move_right(self):
        if self.rect.right < WIDTH:
            self.rect.right += self.velocity

    def shrink(self, reduction_rate):
        if self.width > 10:
            self.width -= reduction_rate
            self.rect.width = self.width


# Ball
ball_radius = 15
ball_speed = 6
ball_rect_size = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(random.randrange(ball_rect_size, WIDTH - ball_rect_size), HEIGHT // 2, ball_rect_size, ball_rect_size)
dx, dy = 1, -1

acceleration = 0.001

game_score = 0
game_score_font = pygame.font.SysFont('comicsansms', 40)
game_score_text = game_score_font.render(f'Your game score is: {game_score}', True, (0, 0, 0))
game_score_rect = game_score_text.get_rect()
game_score_rect.center = (210, 20)

collision_sound = pygame.mixer.Sound('Lab8/catch.mp3')


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    if delta_x > delta_y:
        if rect.top < ball.centery < rect.bottom:
            dy = -dy
            ball.y += dy
        elif rect.left < ball.centerx < rect.right:
            dx = -dx
            ball.x += dx
    elif delta_y > delta_x:
        if rect.left < ball.centerx < rect.right:
            dx = -dx
            ball.x += dx
        elif rect.top < ball.centery < rect.bottom:
            dy = -dy
            ball.y += dy
    return dx, dy

block_list = []
color_list = []

for i in range(10):
    for j in range(4):
        if random.random() < 0.1:
            color = (100, 100, 100)
            unbreakable = True
        else:
            color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))  # Random color for breakable bricks
            unbreakable = False
        block = pygame.Rect(10 + 120 * i, 50 + 70 * j, 100, 50)
        block_list.append((block, unbreakable))
        color_list.append(color)

lose_font = pygame.font.SysFont('comicsansms', 40)
lose_text = lose_font.render('Game Over', True, (255, 255, 255))
lose_text_rect = lose_text.get_rect()
lose_text_rect.center = (WIDTH // 2, HEIGHT // 2)

win_font = pygame.font.SysFont('comicsansms', 40)
win_text = lose_font.render('You win yay', True, (0, 0, 0))
win_text_rect = win_text.get_rect()
win_text_rect.center = (WIDTH // 2, HEIGHT // 2)

paddle = Paddle(150, 100, 20)  # Creating pad

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(background_color)

    for idx, (block, unbreakable) in enumerate(block_list):
        pygame.draw.rect(screen, color_list[idx], block)

    pygame.draw.rect(screen, pygame.Color(255, 255, 255), paddle.rect)
    pygame.draw.circle(screen, pygame.Color(255, 0, 0), ball.center, ball_speed)

    ball.x += ball_radius * dx
    ball.y += ball_speed * dy

    ball_speed += acceleration

    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    if ball.centery < ball_radius + 50:
        dy = -dy
    if paddle.rect.colliderect(ball) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle.rect)

    hitIndex = ball.collidelist([block[0] for block in block_list])

    if hitIndex != -1:
        hitRect, unbreakable = block_list[hitIndex]
        if not unbreakable:
            block_list.pop(hitIndex)
            color_list.pop(hitIndex)
            dx, dy = detect_collision(dx, dy, ball, hitRect)
            game_score += 1
            collision_sound.play()
            paddle.shrink(1)
        else:
            dx, dy = detect_collision(dx, dy, ball, hitRect)

    game_score_text = game_score_font.render(f'Your game score is: {game_score}', True, (255, 255, 255))
    screen.blit(game_score_text, game_score_rect)

    if ball.bottom > HEIGHT:
        screen.fill((0, 0, 0))
        screen.blit(lose_text, lose_text_rect)
    elif not len(block_list):
        screen.fill((255, 255, 255))
        screen.blit(win_text, win_text_rect)

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        paddle.move_left()
    if key[pygame.K_RIGHT]:
        paddle.move_right()

    pygame.display.flip()
    clock.tick(FRAMES_PER_SECOND)
