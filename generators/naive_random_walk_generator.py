import random
from typing import Optional

from game.logic import Logic
from generators.base_generator import BaseGenerator


class NaiveRandomWalkGenerator(BaseGenerator):
    def generate(self, difficulty_steps: int, generations: Optional[int]) -> Logic:
        flasks = self._create_solved_board()
        candidate_logic = Logic(flasks)

        for _ in range(difficulty_steps):
            moves = candidate_logic.get_possible_moves()
            move = random.choice(moves)

            candidate_logic.move(*move)

        return candidate_logic
