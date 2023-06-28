from game import AlienInvasion
from time import sleep


if __name__ == '__main__':

    # Создание экземляра и запуск игры
    # Для выхода из игры нажмите Q
    ai = AlienInvasion()
    sleep(2)
    ai.run_game()
