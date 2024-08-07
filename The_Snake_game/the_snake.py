from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
GRID_WIDTH, GRID_HEIGHT = 32, 24
GRID_SIZE = 20
SCREEN_WIDTH = GRID_WIDTH * GRID_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки - бирюзовый
BORDER_COLOR = (93, 216, 228)

# Цвет яблока - красный
APPLE_COLOR = (255, 0, 0)

# Цвет змейки - зелёный
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Центр поля
CENTER = [(SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)]

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('The Snake')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """
    Базовый класс. Содержит общие атрибуты,
    описывающие позицию и цвет объекта.
    """

    def __init__(self, body_color=None):
        """Инициализация общих атрибутов"""
        self.position = CENTER
        self.body_color = body_color

    def draw(self):
        """Общий метод отрисовки объектов"""
        raise NotImplementedError(
            'Определите метод draw в %s.' % (self.__class__.__name__))

    def draw_cell(self, position, body_color=None, last=False):
        """Общий метод отрисовки объектов"""
        rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, body_color, rect)
        if not last:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Класс, унаследованный от GameObject,
    описывающий яблоко и действия с ним.
    """

    def __init__(self, snake_pos=CENTER, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position(snake_pos)

    def randomize_position(self, snake_pos):
        """Метод задаёт рандомную позицию яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        if self.position in snake_pos:
            self.randomize_position(snake_pos)

    def draw(self):
        """Метод отрисовки яблока"""
        self.draw_cell(self.position, APPLE_COLOR)


class Snake(GameObject):
    """
    Класс, унаследованный от GameObject,
    описывающий змейку и её поведение.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.lenght = 1
        self.positions = [CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод для сброса атрибутов змейки"""
        self.positions = [CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def move(self, apple):
        """Метод описывающий движение змейки"""
        self.head_snake = self.get_head_position()
        head_pos_x, head_pos_y = self.head_snake[0], self.head_snake[1]
        direct_x, direct_y = self.direction[0], self.direction[1]
        self.new_head_snake = (
            (head_pos_x + direct_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_pos_y + direct_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, self.new_head_snake)

        if self.new_head_snake != apple.position:
            self.last = self.positions.pop()
        else:
            ex_apple = pg.Rect(apple.position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, ex_apple)
            apple.randomize_position(snake_pos=self.positions)

    def draw(self):
        """Метод отрисовки змейки"""
        for position in self.positions[:-1]:
            self.draw_cell(position, SNAKE_COLOR)
        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position(), SNAKE_COLOR)
        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR, True)


def handle_keys(game_object):
    """
    Функция для обработки нажатия клавиш,
    чтобы изменить направление движения змейки
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """В функции main происходит обновление состояний объектов"""
    pg.init()  # Инициализация pg
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        # Здесь функции проверки самоукуса и съедания яблока

        if snake.new_head_snake in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
