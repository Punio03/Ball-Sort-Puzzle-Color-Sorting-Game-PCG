import random
from abc import ABC, abstractmethod
from typing import override
from typing import List, Tuple, Optional

from game.logic import Logic, Flask
from solvers.base_solver import BaseSolver


class BaseGenerator(ABC):
    def __init__(
        self, solver: BaseSolver, num_flasks: int, flask_size: int, num_colors: int
    ):
        self.solver = solver
        self.num_flasks = num_flasks
        self.flask_size = flask_size
        self.num_colors = num_colors

    @abstractmethod
    def generate(self, difficulty_steps: int, generations: Optional[int]) -> Logic:
        pass

    def _create_solved_board(self) -> List[Flask]:
        flasks = []
        for c in range(self.num_colors):
            flasks.append(Flask(self.flask_size, [c] * self.flask_size))
        for _ in range(self.num_flasks - self.num_colors):
            flasks.append(Flask(self.flask_size, []))
        return flasks

    @staticmethod
    def _apply_move(flasks, move):
        src, dst = move
        ball = flasks[src].remove()
        flasks[dst].add(ball)

    @staticmethod
    def _get_possible_moves(flasks: List[Flask]) -> List[Tuple[int, int]]:
        moves = []
        for i, src in enumerate(flasks):
            if src.empty():
                continue
            for j, dst in enumerate(flasks):
                if i == j:
                    continue
                if not dst.full():
                    moves.append((i, j))
        return moves

    @staticmethod
    def _smart_choice(
        flasks: List[Flask], moves: List[Tuple[int, int]]
    ) -> Tuple[int, int]:
        better_moves = []
        empty_moves = []

        for m in moves:
            dst_flask = flasks[m[1]]
            if dst_flask.empty():
                empty_moves.append(m)
            else:
                better_moves.append(m)

        if better_moves and random.random() < 0.8:
            return random.choice(better_moves)

        if empty_moves:
            return random.choice(empty_moves)

        return random.choice(moves)


class EvolutionaryGenerator(BaseGenerator):
    @override
    def generate(
        self,
        min_difficulty: int,
        epochs: int,
    ) -> Logic:
        pass
