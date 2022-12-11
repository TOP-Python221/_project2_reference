# pip install schedule
# импорт сторонних пакетов
from schedule import every, run_pending, idle_seconds

# импорт из стандартной библиотеки
from pprint import pprint
from time import sleep

# импорт дополнительных пакетов и модулей
from model import *
from utils import *


class Controller:
    def __init__(self):
        factory = CreatureFactory()
        active_pet = PersistenceManager.read_states('model/states_test.json')
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

    def mainloop(self):
        """"""
        every(4).seconds.do(self.pet.apply_tick_changes)
        while True:
            run_pending()
            print(f'До следующего обновления параметров {idle_seconds():.2} секунд')
            input(' > ')
            sleep(0.1)


# точка входа
if __name__ == '__main__':
    c = Controller()
    print(f'\n{c.pet}')
    pprint(c.pet.state.dict)

    c.mainloop()
