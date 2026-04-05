import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Street Socer Game")

clock = pygame.time.Clock()

# ======================
# PARENT CLASS
# ======================
class GameObject:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))


# ======================
# PLAYER 1
# ======================
class Player(GameObject):

    def move_wasd(self, keys):
        speed = 5

        if keys[pygame.K_a] and self.x > 0:
            self.x -= speed
        if keys[pygame.K_d] and self.x < WIDTH - self.w:
            self.x += speed
        if keys[pygame.K_w] and self.y > 0:
            self.y -= speed
        if keys[pygame.K_s] and self.y < HEIGHT - self.h:
            self.y += speed


# ======================
# PLAYER 2
# ======================
class Enemy(GameObject):

    def move_arrow(self, keys):
        speed = 5

        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.w:
            self.x += speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.h:
            self.y += speed


# ======================
# BALL
# ======================
class Ball(GameObject):

    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, size, color)
        self.vx = 0
        self.vy = 0

    def update(self):

        self.x += self.vx
        self.y += self.vy

        # pantul kiri
        if self.x <= 0:
            self.x = 0
            self.vx = -self.vx

        # pantul kanan
        if self.x >= WIDTH - self.w:
            self.x = WIDTH - self.w
            self.vx = -self.vx

        # pantul atas
        if self.y <= 0:
            self.y = 0
            self.vy = -self.vy

        # pantul bawah
        if self.y >= HEIGHT - self.h:
            self.y = HEIGHT - self.h
            self.vy = -self.vy

        # gesekan
        self.vx *= 0.96
        self.vy *= 0.96


# ======================
# GOAL
# ======================
class Goal(GameObject):
    pass


# ======================
# OBJECT GAME
# ======================
player1 = Player(100, 200, 40, 40, (0,0,255))
player2 = Enemy(650, 200, 40, 40, (255,0,0))

ball = Ball(400, 250, 12, (255,255,255))

goal_left = Goal(0, 200, 30, 100, (255,255,0))
goal_right = Goal(770, 200, 30, 100, (255,255,0))

score1 = 0
score2 = 0

font = pygame.font.SysFont(None,40)

# ======================
# GAME LOOP
# ======================
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # simpan posisi lama player
    old_x1, old_y1 = player1.x, player1.y
    old_x2, old_y2 = player2.x, player2.y

    player1.move_wasd(keys)
    player2.move_arrow(keys)

    ball.update()

    player1_rect = pygame.Rect(player1.x, player1.y, player1.w, player1.h)
    player2_rect = pygame.Rect(player2.x, player2.y, player2.w, player2.h)
    ball_rect = pygame.Rect(ball.x, ball.y, ball.w, ball.h)

    # player tidak bisa menembus bola
    if player1_rect.colliderect(ball_rect):
        player1.x = old_x1
        player1.y = old_y1

    if player2_rect.colliderect(ball_rect):
        player2.x = old_x2
        player2.y = old_y2


    # tendangan player 1 (tanpa diagonal)
    if player1_rect.colliderect(ball_rect):

        dx = ball.x - player1.x
        dy = ball.y - player1.y

        if abs(dx) > abs(dy):
            if dx > 0:
                ball.vx = 3
            else:
                ball.vx = -3
            ball.vy = 0
        else:
            if dy > 0:
                ball.vy = 3
            else:
                ball.vy = -3
            ball.vx = 0


    # tendangan player 2
    if player2_rect.colliderect(ball_rect):

        dx = ball.x - player2.x
        dy = ball.y - player2.y

        if abs(dx) > abs(dy):
            if dx > 0:
                ball.vx = 3
            else:
                ball.vx = -3
            ball.vy = 0
        else:
            if dy > 0:
                ball.vy = 3
            else:
                ball.vy = -3
            ball.vx = 0


    goal_left_rect = pygame.Rect(goal_left.x, goal_left.y, goal_left.w, goal_left.h)
    goal_right_rect = pygame.Rect(goal_right.x, goal_right.y, goal_right.w, goal_right.h)

    # gol kanan
    if ball_rect.colliderect(goal_right_rect):
        score1 += 1
        ball.x = WIDTH//2
        ball.y = HEIGHT//2
        ball.vx = 0
        ball.vy = 0

    # gol kiri
    if ball_rect.colliderect(goal_left_rect):
        score2 += 1
        ball.x = WIDTH//2
        ball.y = HEIGHT//2
        ball.vx = 0
        ball.vy = 0


    # gambar lapangan
    screen.fill((34,139,34))

    player1.draw()
    player2.draw()
    ball.draw()

    goal_left.draw()
    goal_right.draw()

    score_text = font.render(f"{score1} : {score2}", True, (255,255,255))
    screen.blit(score_text,(380,20))

    pygame.display.update()
    clock.tick(60)