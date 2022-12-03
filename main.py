from model import *


# точка входа
if __name__ == '__main__':
    sm = PersistenceManager.read_states()
    kr = PersistenceManager.read_ranges(sm.kind)
    StatesCalculator(kr, sm)

