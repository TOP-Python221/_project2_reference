"""
Модель данных
"""

from abc import ABC

from utils.constants import KindActions

__all__ = [
    'Creature',
    'Body',
    'Mind',
]


class Body:
    """

    """


class Mind:
    """

    """
    @property
    def pattern(self):
        return


class Creature(ABC):
    """

    """
    @property
    def age(self):
        return

    def mainloop(self):
        """"""


class CreatureActions(Creature):
    """

    """
    def run_at_night(self):
        """"""

    def seek_for_honey(self):
        """"""

    def get_warm_on_sun(self):
        """"""
