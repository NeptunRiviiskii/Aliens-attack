import pygame as pg


class Settings:
    """Класс для хранения всех настроек игры"""

    def __init__(self):
        """Инизиализация настроек игры"""

        # Параметры экрана
        self.screen_width = 1920
        self.screen_height = 1080
        # Загрузка изображений
        self.pre_image = pg.image.load('data/images/sky.jpg')
        self.pre_image_ship = pg.image.load('data/images/ship.png')
        self.pre_image_alien = pg.image.load('data/images/alien.png')
        # Подгон размеров фона под размер экрана
        self.bg_image = pg.transform.scale(self.pre_image, (self.screen_width, self.screen_height))
        self.scale = 30
        # Параметры карабля
        self.ship_limit = 3
        # Параметры снаряда
        self.bullet_height = 15
        self.bullet_width = 3
        self.bullet_color = (255, 0, 60)
        # Настройки пришельцев
        self.alien_drop_speed = 5
        self.settings_flag = False
        # Настройки сложности
        self.level_settings = [(5, 10, 1, 1, 1.1),      # dynamic
                               (5, 10, 1, 1, 1.05),     # junior
                               (5, 7, 1, 1, 1.2),       # middle
                               (7, 10, 1, 1, 1.3)]      # senior

    def set_settings(self, n):
        """Выбор настроек игры"""

        self.ship_speed = self.level_settings[n][0]
        self.bullet_speed = self.level_settings[n][1]
        self.alien_speed = self.level_settings[n][2]
        self.alien_direction = self.level_settings[n][3]
        # Темп ускорения игры
        self.speedup_scale = self.level_settings[n][4]

    def increase_speed(self):
        """Повышаение скорости передвижения"""

        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
