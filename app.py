from pprint import pprint

from model import PersistenceManager


# точка входа
if __name__ == '__main__':
    sm = PersistenceManager.read_states()
