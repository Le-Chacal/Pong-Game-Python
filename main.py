from time import sleep

import pygame
import sys
import random

WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

pygame.init()

FPS = 60

PLATFORM_WIDTH = 10
PLATFORM_HEIGHT = 100
PLATFORM_SPEED = 7.5

BALL_WIDTH = 20
BALL_HEIGHT = 20
BALL_SPEED_X = 6
BALL_SPEED_Y = 6
BALL_ACCELERATION = 1

SCORE_L = 0
SCORE_R = 0
SCORE_TO_WIN = 5

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT
        self.speed = PLATFORM_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        self.y += self.speed * -direction

    def update(self):
        if self.y >= HEIGHT - self.height:
            self.y = HEIGHT - self.height
        elif self.y <= 0:
            self.y = 0
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BALL_WIDTH
        self.height = BALL_HEIGHT
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y * random.choice([-1, 1])
        self.acceleration = BALL_ACCELERATION
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.topleft = (self.x, self.y)

    def check_collision(self, platform_l, platform_r):
        if self.y <= 0 or self.y + self.height >= HEIGHT:
            self.speed_x += self.acceleration
            self.speed_y += self.acceleration
            self.speed_y *= -1

        if self.rect.colliderect(platform_l.rect):
            self.speed_x = abs(self.speed_x) + self.acceleration
            self.x = platform_l.x + platform_l.width
            self.rect.topleft = (self.x, self.y)

        if self.rect.colliderect(platform_r.rect):
            self.speed_x = -abs(self.speed_x + self.acceleration)
            self.x = platform_r.x - self.width
            self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        pygame.draw.ellipse(surface, (255, 255, 255), self.rect)

def reset_ball(ball):
    ball.x = WIDTH // 2 - BALL_WIDTH // 2
    ball.y = HEIGHT // 2 - BALL_HEIGHT // 2
    ball.speed_x = BALL_SPEED_X * random.choice([-1, 1])
    ball.speed_y = BALL_SPEED_Y * random.choice([-1, 1])
    ball.rect.topleft = (ball.x, ball.y)

def main():
    global SCORE_L, SCORE_R

    clock = pygame.time.Clock()
    run = True

    platform_l = Platform(50, HEIGHT // 2 - PLATFORM_HEIGHT // 2)
    platform_r = Platform(WIDTH - 50 - PLATFORM_WIDTH, HEIGHT // 2 - PLATFORM_HEIGHT // 2)
    ball = Ball(WIDTH // 2 - BALL_WIDTH // 2, HEIGHT // 2 - BALL_HEIGHT // 2)

    font = pygame.font.Font("pixelify.ttf", 40)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            platform_l.move(1)
        if keys[pygame.K_s]:
            platform_l.move(-1)
        if keys[pygame.K_i]:
            platform_r.move(1)
        if keys[pygame.K_k]:
            platform_r.move(-1)

        ball.move()
        ball.check_collision(platform_l, platform_r)

        if ball.x <= 0:
            SCORE_R += 1
            reset_ball(ball)
        elif ball.x + ball.width >= WIDTH:
            SCORE_L += 1
            reset_ball(ball)

        WIN.fill((0, 0, 0))
        platform_l.update()
        platform_l.draw(WIN)
        platform_r.update()
        platform_r.draw(WIN)
        ball.draw(WIN)


        if SCORE_L >= SCORE_TO_WIN:
            score_text = font.render("WIN  :  LOSE", True, (255, 255, 255))
        elif SCORE_R >= SCORE_TO_WIN:
            score_text = font.render("LOSE  :  WIN", True, (255, 255, 255))
        else:
            score_text = font.render(f"{SCORE_L}  :  {SCORE_R}", True, (255, 255, 255))

        text_width, _ = font.size(f"{SCORE_L}  :  {SCORE_R}")
        WIN.blit(score_text, ((WIDTH - text_width) // 2, 10))

        pygame.display.update()

        if SCORE_L >= SCORE_TO_WIN or SCORE_R >= SCORE_TO_WIN:
            sleep(10)
            break

if __name__ == "__main__":
    main()