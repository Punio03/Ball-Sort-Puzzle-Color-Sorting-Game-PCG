import random
from typing import Optional

from game.logic import Logic, Flask
from generators.base_generator import BaseGenerator


class NaiveReverseWalkGenerator(BaseGenerator):
    def generate(
        self, difficulty_steps: int = 250, generations: Optional[int] = None
    ) -> Logic:
        while True:
            flasks = self._create_solved_board()

            for _ in range(difficulty_steps):
                moves = self._get_possible_moves(flasks)

                if not moves:
                    break

                chosen_move = random.choice(moves)
                self._apply_move(flasks, chosen_move)

            candidate_logic = Logic(flasks)
            is_win, _ = self.solver.solve(candidate_logic)
            if is_win:
                return candidate_logic
