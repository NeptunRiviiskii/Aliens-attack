import pygame as pg


class Ship:
    """Класс для управлениия кораблем"""

    def __init__(self, ai_game):
        """Инициализирует корабль и его параметры"""

        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.pre_image = ai_game.settings.pre_image_ship
        # Подгон размера изображения корабля
        self.pre_height, self.pre_width = self.pre_image.get_size()
        self.height, self.width = self.pre_height/ai_game.settings.scale, self.pre_width/ai_game.settings.scale
        self.image = pg.transform.scale(self.pre_image, (self.height, self.width))
        # Получене координат и привязка к низу экрана
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

    def blit_me(self):
        """Рисует корабль в текущей позиции"""

        self.screen.blit(self.image, self.rect)

    def update(self):
        """Перемещение корабля"""

        key = pg.key.get_pressed()
        if key[pg.K_RIGHT] and self.rect.right < self.settings.screen_width:
            self.rect.x += self.settings.ship_speed
        if key[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed
        # Можно включить при желании
        # if key[pg.K_UP] and self.rect.y > self.settings.screen_height * 0.75:
        #     self.rect.y -= self.settings.ship_speed
        # if key[pg.K_DOWN] and self.rect.y + 2537/30 < self.settings.screen_height:
        #     self.rect.y += self.settings.ship_speed

    def center_ship(self):
        """Перемещение корабля в центр внизу"""

        self.rect.midbottom = self.screen_rect.midbottom