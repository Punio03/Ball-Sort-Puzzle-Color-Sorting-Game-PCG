from abc import ABC, abstractmethod
from typing import override

from game.logic import Logic
from solvers.base_solver import BaseSolver


class BaseGenerator(ABC):
    def __init__(self, solver: BaseSolver, num_flasks: int, num_colors: int):
        self.solver = solver
        self.num_flasks = num_flasks
        self.num_colors = num_colors

    @abstractmethod
    def generate(self, size: int, min_difficulty: int) -> Logic:
        pass

class EvolutionaryGenerator(BaseGenerator):
    def __init__(self, solver, num_flasks, num_colors):
        super().__init__(solver, num_flasks, num_colors)
    
    @override
    def generate(
        self,
        size: int,
        min_difficulty: int,
        epochs: int,
        
    ) -> Logic:
        pass