from pathlib import Path
from sys import path

from .states import StatesManager

__all__ = [
    'PersistenceManager',
]



class PersistenceManager:
    """

    """
    default_states_path = Path(path[0]) / 'model/states.json'

    @classmethod
    def read_states(cls) -> StatesManager:
        """"""

    @classmethod
    def write_states(cls):
        """"""

