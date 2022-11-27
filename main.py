from model import *

# перечислены в переменной __all__ пакета model
StatesCalculator()
PersistenceManager()

# не перечислен в переменной __all__ пакета model — вызовет исключение
StatesManager()
