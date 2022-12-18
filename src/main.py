# pip install schedule
# импорт сторонних пакетов
from schedule import every

# импорт из стандартной библиотеки
from pprint import pprint
from threading import Event

# импорт дополнительных пакетов и модулей
from src import *


class Controller:
    def __init__(self):
        factory = CreatureFactory()
        active_pet = PersistenceManager.read_active('../data/tests/active_empty_dict.json')
        if active_pet:
            factory.creature_data = active_pet
            self.pet = factory.revive_creature()
        else:
            factory.kind = self._get_new_kind()
            factory.name = self._get_new_name()
            self.pet = factory.new_creature()

    def _get_new_kind(self) -> Kind:
        """Получает из stdin вид нового питомца."""
        # self.show_kinds()
        # kind = input()
        kind = Kind('cat')
        return kind

    def _get_new_name(self) -> str:
        """Получает из stdin имя нового питомца."""
        # name = input()
        name = 'Марсик'
        return name

    def mainloop(self, tick_interval: int = 900, thread_interval: float = 90):
        """"""
        every(tick_interval).seconds.do(self.pet.apply_tick_changes)
        stop_background = Event()
        self.pet.continuous_tick(stop_background, thread_interval)

        # цикл обработки команд
        while True:
            command = input(' > ').lower()

            if command == 'quit':
                break

            elif command == 'watch':
                self.pet.action()

        stop_background.set()


# точка входа
if __name__ == '__main__':
    c = Controller()
    print(f'\n{c.pet}')
    pprint(c.pet.state.dict)

    c.mainloop(5, 1)

    pprint(c.pet.state.dict)
