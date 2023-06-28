import sys
from time import sleep
import pygame as pg
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pg.init()
        self.settings = Settings()
        # полноэкранное отображение
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # код неполноэкранного отображения
#        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Инопланетное вторжение")
        # создание игровой статистики
        self.stats = GameStats(self)
        # Создание игровых объектов
        self.ship = Ship(self)
        self.bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()
        self._create_fleet()
        # Создание игровых кнопок
        self._create_buttons()

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            # Отслеживание событий клавиатуры и мыши
            self._check_events()
            if self.stats.game_active:
                # Обновление игрвого процесса
                self.ship.update()
                self._update_bullets()
                self._update_alien()
            # Обновление экрана
            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатие клавиш и события мыши"""

        # Отслеживание событий клавиатуры и мыши
        key = pg.key.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT or key[pg.K_q]:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self._check_buttons(mouse_pos)
        self._check_collide_mouse(mouse_pos)
        if key[pg.K_SPACE]:
            self._fire_bullet()
        if key[pg.K_p] and not self.stats.game_active:
            self._start_game()

    def _check_collide_mouse(self, mouse_pos):
        """Праверка наведения на кнопки, исполнение анимации"""

        # Проверка кнопки Play
        if self.buttons[0].rect.collidepoint(mouse_pos) and self.buttons[0].color_style == 'standard':
            self.buttons[0].reverse_color()
        elif not self.buttons[0].rect.collidepoint(mouse_pos) and self.buttons[0].color_style == 'reverse':
            self.buttons[0].set_color()
        # Проверка остальных кнопок
        self._check_buttons_status(mouse_pos)

    def _check_buttons_status(self, mouse_pos):
        """Праверка наведения на кнопки сложности и исполнение анимации"""

        for button in self.buttons[1:]:
            # Проверка наведения на кнопку
            if button.rect.collidepoint(mouse_pos):
                # Проверка была ли нажата это кнопка ранее
                if button.set_flag:
                    # Проверка цветового стиля (обычный или инверсия)
                    if button.color_style == 'standard':
                        button.reverse_color((255, 0, 0))
                else:
                    if button.color_style == 'standard':
                        button.reverse_color()
            elif not button.rect.collidepoint(mouse_pos):
                if button.set_flag:
                    if button.color_style == 'reverse':
                        button.set_color((255, 0, 0))
                else:
                    button.set_color()

    def _check_buttons(self, mouse_pos):
        """Запуск игрового процесса при нажитии на Play
         и анализ выбранной уровня сложности"""

        play_button_clicked = self.buttons[0].rect.collidepoint(mouse_pos)
        if not self.stats.game_active:
            # Установка настроек если нажата кнопка Play
            if play_button_clicked:
                if not self.settings.settings_flag:
                    # Сброс игровых настроек
                    self.settings.set_settings(0)
                    # Запуск игрового процесса
                    self._start_game()
                    # Скрытие указателя мыши
                    pg.mouse.set_visible(False)
                else:
                    # Запуск игрового процесса
                    self._start_game()
                    # Скрытие указателя мыши
                    pg.mouse.set_visible(False)
            else:
                # Установка настроек в зависимости от выбранного уровня сложности
                for n, button in enumerate(self.buttons[1:], 1):
                    if button.rect.collidepoint(mouse_pos):
                        self.settings.set_settings(n)
                        self.settings.settings_flag = True
                        button.set_flag = True
                    else:
                        if self.settings.settings_flag:
                            button.set_flag = False

    def _create_buttons(self):
        """Создание кнопок игры"""

        play_button = Button(self, 'Play', self.screen.get_rect().center)
        jun_button = Button(self, 'Junior', (play_button.rect.width, play_button.rect.height*0.85))
        mid_button = Button(self, 'Middle', (2.5*play_button.rect.width, play_button.rect.height*0.85))
        sen_button = Button(self, 'Senior', (4*play_button.rect.width, play_button.rect.height*0.85))
        # Группировка кнопок
        self.buttons = [play_button, jun_button, mid_button, sen_button]

    def _start_game(self):
        """Запуск игрового процесса"""

        # Сброс статистики и перезапуск игры
        self.stats.reset_stats()
        self.stats.game_active = True
        self.settings.settings_flag = False
        # Очистка игрового поля
        self.aliens.empty()
        self.bullets.empty()
        # Создание флота и обновление игрового процесса
        self._create_fleet()
        self.ship.center_ship()

    def _update_alien(self):
        """Обновление позиции и напраления пришельцев"""

        self._check_fleet_edges()
        self.aliens.update()
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Реагирует на достижение края экрана пришельцем"""

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Изменения направления флота и сдвиг вниз"""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed
        self.settings.alien_direction *= -1

    def _calculation_fleet(self, n):
        """Расчет количества ккараблей пришельцев"""

        # Получение габаритов корабля по созданному экземпляру
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        # Расчёт свободного пространства под пришельцев
        available_space_y = self.settings.screen_height*0.5 - alien_height
        available_space_x = self.settings.screen_width - (n*alien_width)
        # Вчисление количества пришльцев
        number_aliens_x = available_space_x // (n*alien_width)
        number_aliens_y = int(available_space_y // (n/2*alien_height))
        return alien_width, alien_height, number_aliens_x, number_aliens_y

    def _create_fleet(self):
        """Создание флота вторжения"""

        # Масштаб для регулировки расстояния между караблями
        n = 3
        alien_width, alien_height, number_aliens_x, number_aliens_y = self._calculation_fleet(n)
        # Создание флота пришельцев
        for num_y in range(number_aliens_y):
            for num_x in range(number_aliens_x):
                alien = Alien(self)
                # Выбор позиций пришельцев
                alien.x = alien_width + n * alien_width * num_x
                alien.rect.x = alien.x
                alien.y = alien_height + n / 2 * alien_height * num_y
                alien.rect.y = alien.y
                self.aliens.add(alien)

    def _ship_hit(self):
        """Обработка столкновений с пришельцем"""

        if self.stats.ships_limit > 1:
            # Обновление экрана
            self._update_screen()
            # Минус одна жизнь
            self.stats.ships_limit -= 1
            # Удаление кораблей и пуль
            self.aliens.empty()
            self.bullets.empty()
            # Созадние нового флота и коробля
            self._create_fleet()
            self.ship.center_ship()
            # Пауза
            sleep(1)
        else:
            self.stats.game_active = False
            pg.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Проверяет косание пришельцев низа экрана"""

        screen_rect = self.screen.get_rect().bottom
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect:
                self._ship_hit()
                break

    def _update_screen(self):
        """Обновление изображения на экране и его отображение"""
        # Отображение последнего игрового экрана

        # При каждом рпоходе цикла перерисовывается экран
        self.screen.blit(self.settings.bg_image, (0, 0))
        self.ship.blit_me()
        # Отрисовка снарядов
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Отрисовка вражеских кораблей
        self.aliens.draw(self.screen)
        # Отображение кнопок
        if not self.stats.game_active:
            [button.draw_button() for button in self.buttons]
        # Отображение последнего игрового экрана
        pg.display.flip()

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в новую группу"""

        if not self.bullets:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        if self.bullets and self.ship.rect.y - self.bullets.sprites()[-1].rect.y > 500:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновление позиций снарядов и удаление вышедших за край"""

        # Обновление позоций снарядов
        self.bullets.update()

        # Удаление ненужных снарядов
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_alien_bullet_collisions()

    def _check_alien_bullet_collisions(self):
        """Проверка попаданий в пришельцев и удаление пуль и кораблей"""

        pg.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # Очистка поля от снарядов и создание нового флота, повышение сложности
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
