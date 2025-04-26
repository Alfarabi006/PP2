import pygame
import random
import time
import psycopg2

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    database="postgres",
    user="omar",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Получение имени пользователя
username = input("Enter your username: ")
cur.execute("SELECT id FROM users WHERE username = %s", (username,))
user = cur.fetchone()

if not user:
    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
    user_id = cur.fetchone()[0]
    conn.commit()
else:
    user_id = user[0]

# Получение текущего уровня пользователя (последняя запись)
cur.execute("""
    SELECT level 
    FROM user_score 
    WHERE user_id = %s 
    ORDER BY timestamp DESC 
    LIMIT 1
""", (user_id,))
last_level = cur.fetchone()

if last_level:
    level = last_level[0]
    print(f"Welcome back, {username}! Last recorded level: {level}")
else:
    level = 1
    print(f"Welcome, {username}! Starting from level 1.")

# Инициализация игры
pygame.init()
width = 500
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game with Levels")
clock = pygame.time.Clock()
done = False
score = 0
level = 1

coor_head = [100, 100]
coor_body = [[30, 100], [40, 100], [50, 100], [60, 100], [70, 100], [80, 100], [90, 100], [100, 100]]

def generate_apple():
    while True:
        apple_x = random.randrange(0, width // 10) * 10
        apple_y = random.randrange(0, height // 10) * 10
        new_apple = [apple_x, apple_y]
        if new_apple not in coor_body and new_apple != coor_head:
            weight = random.choice([10, 20, 30])
            color = {10: (0, 255, 0), 20: (255, 165, 0), 30: (255, 0, 0)}[weight]
            timer = random.randint(10, 15)
            return {"pos": new_apple, "weight": weight, "color": color, "spawn_time": time.time(), "timer": timer}

coor_apple = generate_apple()
eaten = False
next_dir = "r"
direc = "r"

def score_update(font, size, color, level):
    score_font = pygame.font.SysFont(font, size)
    score_render = score_font.render(f"Score: {score}  Level: {level}", True, color)
    screen.blit(score_render, (10, 10))

def game_over_message(font, size, color):
    global done
    cur.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)", (user_id, score, level))
    conn.commit()
    game_over_font = pygame.font.SysFont(font, size)
    game_over_surface = game_over_font.render(f"Game Over! Final Score: {score}", True, color)
    screen.blit(game_over_surface, (50, height // 2))
    pygame.display.update()
    pygame.time.delay(3000)
    done = True

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                next_dir = "r"
            if event.key == pygame.K_LEFT:
                next_dir = "l"
            if event.key == pygame.K_UP:
                next_dir = "u"
            if event.key == pygame.K_DOWN:
                next_dir = "d"
            if event.key == pygame.K_p:
                # Сохранение состояния в БД
                cur.execute(
                    "INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)",
                    (user_id, score, level)
                )
                conn.commit()
                print("Game paused. Progress saved.")

                # Пауза — ждём нажатия любой клавиши для продолжения
                paused = True
                pause_font = pygame.font.SysFont("times new roman", 30)
                pause_text = pause_font.render("Paused - Press any key to continue", True, (255, 255, 0))
                screen.blit(pause_text, (50, height // 2))
                pygame.display.update()

                while paused:
                    for pause_event in pygame.event.get():
                        if pause_event.type == pygame.KEYDOWN:
                            paused = False
                        elif pause_event.type == pygame.QUIT:
                            paused = False
                            done = True

    for seg in coor_body[:-1]:
        if coor_head == seg:
            game_over_message("times new roman", 20, (255, 0, 0))

    screen.fill((0, 0, 0))

    if next_dir == "r" and direc != "l": direc = "r"
    if next_dir == "l" and direc != "r": direc = "l"
    if next_dir == "u" and direc != "d": direc = "u"
    if next_dir == "d" and direc != "u": direc = "d"

    if direc == "r": coor_head[0] += 10
    if direc == "l": coor_head[0] -= 10
    if direc == "u": coor_head[1] -= 10
    if direc == "d": coor_head[1] += 10

    if coor_head[0] < 0 or coor_head[0] >= width or coor_head[1] < 0 or coor_head[1] >= height:
        game_over_message("times new roman", 20, (255, 0, 0))

    new_coor = list(coor_head)
    coor_body.append(new_coor)
    coor_body.pop(0)

    if time.time() - coor_apple["spawn_time"] >= coor_apple["timer"]:
        coor_apple = generate_apple()

    if coor_head == coor_apple["pos"]:
        eaten = True
        score += coor_apple["weight"]

    if eaten:
        coor_body.insert(0, coor_body[0])
        coor_apple = generate_apple()
        eaten = False

    level = score // 30 + 1
    speed = 5 + (level - 1)

    pygame.draw.rect(screen, coor_apple["color"], pygame.Rect(coor_apple["pos"][0], coor_apple["pos"][1], 10, 10))
    for el in coor_body:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(el[0], el[1], 10, 10))
    pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(coor_head[0], coor_head[1], 10, 10))

    score_update("times new roman", 20, (128, 128, 128), level)
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
conn.close()
