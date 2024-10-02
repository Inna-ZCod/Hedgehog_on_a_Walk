import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана и панели
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
GAME_FIELD_WIDTH = 600
SIDE_PANEL_WIDTH = (SCREEN_WIDTH - GAME_FIELD_WIDTH) // 2

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAIN_GREEN = (50, 205, 50)
DARK_GREEN_PANEL = (34, 139, 34)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (0, 100, 0)

# Настройки игрока
PLAYER_SPEED = 5
PLAYER_SIZE = (60, 60)
LIFE_ICON_SIZE = (100, 100)

# Настройки игры
OBSTACLE_SPEED = 5
OBSTACLE_FREQUENCY = 600
INVINCIBILITY_FRAMES = 30  # Новая переменная для неуязвимости после столкновения

# Экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ёжик на прогулке")

# Загрузка спрайтов
player_img_left = pygame.image.load('egle.png')
player_img_left = pygame.transform.scale(player_img_left, PLAYER_SIZE)
player_img_right = pygame.transform.flip(player_img_left, True, False)
apple_image = pygame.image.load('aple_green.png')
apple_image = pygame.transform.scale(apple_image, (40, 40))
brick_texture = pygame.image.load('briks3.png')

egle_start_image = pygame.image.load('egle_start.png')
egle_start_image = pygame.transform.scale(egle_start_image, (200, 200))  # Подгонка изображения под круг

# Шрифты
font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 36)

# Набор эллипсов для клякс (увеличенные размеры и новые фигуры)
blot_shapes = [
    (160, 80), (200, 100), (120, 60), (180, 90), (140, 70), (220, 110)
]
blot_colors = [LIGHT_GREEN, DARK_GREEN, (34, 139, 34), (0, 128, 0)]


# Классы игровых объектов
class GameObject:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        pass

    def is_off_screen(self):
        return self.rect.y > SCREEN_HEIGHT


class GrassBlot(GameObject):
    def __init__(self, x, y):
        shape = random.choice(blot_shapes)
        color = random.choice(blot_colors)
        super().__init__(x, y, shape[0], shape[1], OBSTACLE_SPEED)
        self.color = color

    def draw(self):
        pygame.draw.ellipse(screen, self.color, self.rect)


class Player(GameObject):
    def __init__(self):
        super().__init__(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE[1] - 10, PLAYER_SIZE[0], PLAYER_SIZE[1], 0)
        self.direction = 'right'

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(SIDE_PANEL_WIDTH, min(self.rect.x, SCREEN_WIDTH - SIDE_PANEL_WIDTH - self.rect.width))

    def draw(self):
        img = player_img_right if self.direction == 'right' else player_img_left
        screen.blit(img, (self.rect.x, self.rect.y))


class Obstacle(GameObject):
    def __init__(self):
        width = random.randint(60, 200)
        x = random.randint(SIDE_PANEL_WIDTH, SCREEN_WIDTH - SIDE_PANEL_WIDTH - width)
        super().__init__(x, -60, width, 60, OBSTACLE_SPEED)

    def draw(self):
        brick_fragment = pygame.transform.scale(brick_texture, (self.rect.width, self.rect.height))
        screen.blit(brick_fragment, self.rect)


class Bonus(GameObject):
    def __init__(self):
        x = random.randint(SIDE_PANEL_WIDTH, SCREEN_WIDTH - SIDE_PANEL_WIDTH - 40)
        y = random.randint(-100, -40)
        super().__init__(x, y, 40, 40, OBSTACLE_SPEED)

    def draw(self):
        screen.blit(apple_image, self.rect)


def draw_lives(lives):
    life_img = pygame.transform.scale(player_img_right, LIFE_ICON_SIZE)
    for i in range(lives):
        x_position = (SIDE_PANEL_WIDTH - LIFE_ICON_SIZE[0]) // 2
        y_position = 50 + i * 110
        screen.blit(life_img, (x_position, y_position))


def draw_score(score):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(f"{score}", True, WHITE)
    screen.blit(text_surface, (SCREEN_WIDTH - SIDE_PANEL_WIDTH + 100, 50))


def draw_labels():
    font = pygame.font.Font(None, 36)
    lives_label = font.render("Жизни:", True, WHITE)
    score_label = font.render("Очки:", True, WHITE)
    screen.blit(lives_label, (SIDE_PANEL_WIDTH // 2 - lives_label.get_width() // 2, 10))
    screen.blit(score_label, (SCREEN_WIDTH - SIDE_PANEL_WIDTH + 20, 10))


# Функция отображения стартового экрана
def show_start_screen():
    running = True
    while running:
        screen.fill(MAIN_GREEN)

        # Рисуем белый круг
        pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 150)

        # Рисуем изображение в центре круга
        screen.blit(egle_start_image, (SCREEN_WIDTH // 2 - egle_start_image.get_width() // 2,
                                       SCREEN_HEIGHT // 2 - egle_start_image.get_height() // 2 - 20))

        # Отображение текста
        text_large = font_large.render("Начнем?", True, WHITE)
        text_medium = font_medium.render("(нажми пробел)", True, WHITE)

        # Рисуем зеленую плашку для текста
        text_background_height = text_large.get_height() + text_medium.get_height() + 10
        pygame.draw.rect(screen, MAIN_GREEN,
                         (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 100, 240, text_background_height))

        # Отображение текста поверх плашки
        screen.blit(text_large, (SCREEN_WIDTH // 2 - text_large.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(text_medium, (
            SCREEN_WIDTH // 2 - text_medium.get_width() // 2, SCREEN_HEIGHT // 2 + 100 + text_large.get_height()))

        # Обработка нажатия клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    return True


# Функция отображения финишного экрана
def show_game_over_screen(score):
    running = True
    while running:
        screen.fill(MAIN_GREEN)

        # Отображение текста
        text_large1 = font_large.render("Ёжик заблудился на прогулке", True, WHITE)
        text_large2 = font_large.render("и растерял все яблоки...", True, WHITE)
        text_medium = font_medium.render(f"Ваш счет: {score}", True, WHITE)
        text_small = font_medium.render("(нажми пробел, чтобы начать заново)", True, WHITE)

        # Отрисовка текста
        screen.blit(text_large1, (SCREEN_WIDTH // 2 - text_large1.get_width() // 2, SCREEN_HEIGHT // 2 - 120))
        screen.blit(text_large2, (SCREEN_WIDTH // 2 - text_large2.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(text_medium, (SCREEN_WIDTH // 2 - text_medium.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(text_small, (SCREEN_WIDTH // 2 - text_small.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        # Обработка нажатия клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False  # Выходим из экрана завершения

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    return True


# Основной игровой цикл
def start_game():
    if not show_start_screen():
        return  # Если пользователь закрыл игру - выйти
    while True:
        player = Player()
        obstacles = []
        bonuses = []
        grass_blots = []
        lives = 3
        score = 0
        game_started = False
        invincibility_timer = 0  # Таймер неуязвимости
        last_life_added_score = 0  # Для добавления жизни за каждые 10 очков

        pygame.time.set_timer(pygame.USEREVENT, OBSTACLE_FREQUENCY)

        while lives > 0:
            screen.fill(MAIN_GREEN)
            pygame.draw.rect(screen, DARK_GREEN_PANEL, (0, 0, SIDE_PANEL_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, DARK_GREEN_PANEL,
                             (SCREEN_WIDTH - SIDE_PANEL_WIDTH, 0, SIDE_PANEL_WIDTH, SCREEN_HEIGHT))

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.USEREVENT and game_started:
                    obstacles.append(Obstacle())
                    bonus = Bonus()
                    while any(ob.rect.colliderect(bonus.rect) for ob in obstacles):
                        bonus = Bonus()
                    bonuses.append(bonus)
                    grass_blots.append(
                        GrassBlot(random.randint(SIDE_PANEL_WIDTH + 40, SCREEN_WIDTH - SIDE_PANEL_WIDTH - 40),
                                  random.randint(-100, -40)))

            keys = pygame.key.get_pressed()
            if not game_started:
                if keys[pygame.K_SPACE]:
                    game_started = True
                else:
                    draw_lives(lives)
                    draw_labels()
                    pygame.display.flip()
                    continue

            dx = 0
            if keys[pygame.K_LEFT]:
                player.direction = 'left'
                dx = -PLAYER_SPEED
            elif keys[pygame.K_RIGHT]:
                player.direction = 'right'
                dx = PLAYER_SPEED

            player.move(dx)

            # Отрисовка
            for blot in grass_blots[:]:
                blot.move()
                blot.draw()
                if blot.is_off_screen():
                    grass_blots.remove(blot)

            for obstacle in obstacles[:]:
                obstacle.move()
                obstacle.draw()
                if obstacle.is_off_screen():
                    obstacles.remove(obstacle)

            for bonus in bonuses[:]:
                bonus.move()
                bonus.draw()
                if bonus.is_off_screen():
                    bonuses.remove(bonus)

            player.draw()

            # Проверка столкновений с препятствиями (с учётом неуязвимости)
            if invincibility_timer == 0:
                for obstacle in obstacles[:]:
                    if obstacle.rect.colliderect(player.rect):
                        lives -= 1
                        invincibility_timer = INVINCIBILITY_FRAMES  # Включаем неуязвимость
                        break

                        # Проверка столкновений с бонусами
            for bonus in bonuses[:]:
                if bonus.rect.colliderect(player.rect):
                    score += 1
                    bonuses.remove(bonus)

                    # Счётчик неуязвимости
            if invincibility_timer > 0:
                invincibility_timer -= 1

                # Добавление жизни за каждые 10 очков
            if score // 10 > last_life_added_score:
                lives += 1
                last_life_added_score = score // 10

                # Отрисовка панели
            draw_lives(lives)
            draw_score(score)
            draw_labels()

            pygame.display.flip()
            pygame.time.Clock().tick(60)

            # Переход на финишный экран после окончания игры
        if not show_game_over_screen(score):
            break  # Выйти из игры, если закрыли игру


if __name__ == "__main__":
    start_game()