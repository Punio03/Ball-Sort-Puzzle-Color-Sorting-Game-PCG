from abc import abstractmethod, ABC
from typing import Tuple, List

from game.logic import Logic


class BaseSolver(ABC):
    @staticmethod
    def _get_canonical(board_data):
        return tuple(sorted([tuple(t) for t in board_data]))

    @abstractmethod
    def solve(self, logic: Logic) -> Tuple[bool, List[Tuple[int, int]]]:
        pass
