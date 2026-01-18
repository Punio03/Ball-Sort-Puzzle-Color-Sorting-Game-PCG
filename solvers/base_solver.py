from abc import abstractmethod, ABC
from typing import Tuple, List

from game.logic import Logic


class BaseSolver(ABC):
    @abstractmethod
    def solve(self, logic: Logic) -> Tuple[bool, List[Tuple[int, int]]]:
        pass
