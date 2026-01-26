import pygame as pg
import sys
import random
import cv2
import model as m


WIDTH, HEIGHT = 1280, 720

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 140
BALL_SIZE = 30

PADDLE_SPEED = 15
BALL_SPEED_X = 15
BALL_SPEED_Y = 15


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Game")
clock = pg.time.Clock()


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("can't open camera")
    running = False


ball = pg.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
player = pg.Rect(WIDTH - PADDLE_WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent = pg.Rect(20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))


player_score = 0
opponent_score = 0
font = pg.font.Font(None, 74)

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    pg.time.delay(500)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))


running = True
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if 'cap' in locals() and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            state = m.get_hand_state(frame)
            cv2.imshow("Webcam", frame)

            if state:
                if state == [0, 0, 0, 0, 0]:
                    player.y += PADDLE_SPEED
                elif state == [1, 0, 0, 0, 0]:
                    player.y -= PADDLE_SPEED

    player.top = max(0, player.top)
    player.bottom = min(HEIGHT, player.bottom)

    if opponent.centery < ball.centery:
        opponent.y += PADDLE_SPEED
    if opponent.centery > ball.centery:
        opponent.y -= PADDLE_SPEED


    opponent.top = max(0, opponent.top)
    opponent.bottom = min(HEIGHT, opponent.bottom)

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1


    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


    if ball.left <= 0:
        player_score += 1
        ball_restart()

    if ball.right >= WIDTH:
        opponent_score += 1
        ball_restart()


    screen.fill(BLACK)
    pg.draw.rect(screen, WHITE, player)
    pg.draw.rect(screen, WHITE, opponent)
    pg.draw.ellipse(screen, WHITE, ball)
    pg.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))


    player_text = font.render(f"{player_score}", True, WHITE)
    screen.blit(player_text, (WIDTH // 2 + 20, 10))
    opponent_text = font.render(f"{opponent_score}", True, WHITE)
    screen.blit(opponent_text, (WIDTH // 2 - opponent_text.get_width() - 20, 10))


    pg.display.flip()
    clock.tick(60) 


    if cv2.waitKey(1) & 0xFF == ord('q'):
        running = False


if 'cap' in locals() and cap.isOpened():
    cap.release()
cv2.destroyAllWindows()
pg.quit()
sys.exit()
