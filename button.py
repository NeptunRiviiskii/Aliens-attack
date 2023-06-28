import pygame.font


class Button:
    """Класс предстовляющий кнопку (универсальную)"""

    def __init__(self, ai_game, msg, pos):
        """Инициализация параметров кнопки"""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # Размеры и свойства
        self.widht, self.height = 200, 50
        self.font = pygame.font.SysFont(None, 48)
        # Построение и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.widht, self.height)
        self.rect.center = pos
        # Текст кнопки
        self.msg = msg
        # Цвет кнопки
        self.set_color()
        # Индикиция того, что выбрали эту кнопку
        self.set_flag = False

    def _prep_msg(self, text_color=None):
        """Созадние кнопки"""

        if not text_color:
            self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        else:
            self.msg_image = self.font.render(self.msg, True, text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def set_color(self, text_color=None):
        """Установка цвета кнопки"""

        self.button_color = (0, 0, 105)
        self.text_color = (255, 255, 255)
        self._prep_msg(text_color)
        self.color_style = 'standard'

    def reverse_color(self, text_color=None):
        """Инверсия цвета кнопки"""

        self.button_color = tuple(255 - c for c in self.button_color)
        self.text_color = tuple(255 - c for c in self.text_color)
        self._prep_msg(text_color)
        self.color_style = 'reverse'

    def draw_button(self):
        """Отрисовка кнопки"""

        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
