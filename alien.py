import pygame as pg
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс предаствляющий пришельца"""

    def __init__(self, ai_game):
        """Инициализирует пришельца и его параметры"""

        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.settings = ai_game.settings
        # Загружает изображение пришельца
        self.pre_image = ai_game.settings.pre_image_alien
        # Подгон размера изображения пришельца
        self.pre_height, self.pre_width = self.pre_image.get_size()
        self.height, self.width = self.pre_height/ai_game.settings.scale, self.pre_width/ai_game.settings.scale
        self.image = pg.transform.scale(self.pre_image, (self.height, self.width))
        # Получение координат пришельца
        self.rect = self.image.get_rect()

        # Создание пришельца в левом верхнем углу
        self.rect.x = 0
        self.rect.y = 0

        # Сохранение точной горизонтальной позиции пришельца
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def draw_alien(self):
        """Отрисовка пришельца"""

        self.screen.blit(self.image, self.rect)

    def update(self):
        """Перемещение пришельца вниз и вправо и влево"""

        self.x += self.settings.alien_speed * self.settings.alien_direction
        self.rect.x = self.x

    def check_edges(self):
        """Возвращает True если достигнут край экрана"""

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right - self.width/4 or self.rect.left <= self.width/4:
            return True
