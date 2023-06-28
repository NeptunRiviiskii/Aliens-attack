class GameStats:
    """Отслеживание статистики игры"""

    def __init__(self, ai_game):
        """Инициализация статистики"""

        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""

        # Количество жизней
        self.ships_limit = self.settings.ship_limit
