import os
import pygame

os.environ['SDL_VIDEO_WINDOW_POS'] = "200,30"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('brick.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('paddle.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move_left(self):
        self.rect.x -= 20

    def move_right(self):
        self.rect.x += 20


class Ball(pygame.sprite.Sprite):
    BALL_SPEED = 8
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.direction_x = 1
        self.direciton_y = 1
        self.image = pygame.image.load('ball.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def flip_direction_x(self):
        self.direction_x *= -1

    def flip_direction_y(self):
        self.direciton_y *= -1

    def leaves_screen_bottom(self):
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH:
            self.flip_direction_x()
        if self.rect.y < 0:
            self.flip_direction_y()

        return self.rect.y > SCREEN_HEIGHT

    def move(self):
        self.rect.x += self.BALL_SPEED * self.direction_x
        self.rect.y += self.BALL_SPEED * self.direciton_y


def main():
    pygame.init()
    pygame.font.init()
    game_font = pygame.font.SysFont('', 30)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Breakout Game | codingboost.com')
    clock = pygame.time.Clock()

    paddle = Paddle(100, 550)
    ball = Ball(250, 250)

    brick_list = pygame.sprite.Group()
    paddle_list = pygame.sprite.Group()
    ball_list = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    paddle_list.add(paddle)
    ball_list.add(ball)
    all_sprites.add(paddle)
    all_sprites.add(ball)

    for i in range(0, 10):
        for j in range(0, 3):
            brick = Brick(70 + i * 70, 20 + j * 50)
            brick_list.add(brick)
            all_sprites.add(brick)

    score = 0
    score_surface = None

    done = False
    while not done:
        screen.fill(GRAY)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move_left()

        if keys[pygame.K_RIGHT]:
            paddle.move_right()

        if keys[pygame.K_ESCAPE]:
            done = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        if pygame.sprite.collide_mask(ball, paddle):
            ball.flip_direction_y()

        collided_bricks = pygame.sprite.groupcollide(
            brick_list, ball_list, True, False, pygame.sprite.collide_mask)
        if collided_bricks:
            ball.flip_direction_y()
            score += len(collided_bricks)

        if score_surface is None or collided_bricks:
            score_surface = game_font.render(
                'Score: %d' % (score), False, GREEN)

        ball.move()
        if ball.leaves_screen_bottom():
            # reset the ball position
            ball.rect.x = 200
            ball.rect.y = 300

        all_sprites.update()
        all_sprites.draw(screen)
        screen.blit(score_surface, (50, 240))
        pygame.display.update()
        clock.tick(60)

main()