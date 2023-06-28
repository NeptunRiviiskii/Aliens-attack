import pygame as pg
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс представляющий снаряд выпущенный караблем"""

    def __init__(self, ai_game):
        """Инициализация снаряда и его параметров"""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        # Создание снаряда и перемещение в нужную позицию
        self.rect = pg.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        # Позиция снаряда хранится в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        """перемещение снаряда вверх по экрану"""

        # Обновление снаряда в вещественном формате
        self.y -= self.settings.bullet_speed
        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывод снаряда на экран"""

        pg.draw.rect(self.screen, self.color, self.rect)
